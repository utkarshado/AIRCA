"""
api/routes.py - FastAPI router exposing the coding agent over HTTP.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import StreamingResponse

from app.agents.coding_agent import CodingAgent
from app.rag.retriever import Retriever
from app.rag.vector_store import VectorStore
from app.memory.conversation_memory import ConversationMemory

router = APIRouter()

# ── Shared singletons (swap for proper DI in production) ──────────────────────
_vector_store = VectorStore()
_retriever = Retriever(vector_store=_vector_store)

# One memory object per session — in production, key this by session/user ID
_memory = ConversationMemory()
_agent = CodingAgent(retriever=_retriever, memory=_memory)


# ── Request / Response models ──────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: str


class IndexRequest(BaseModel):
    codebase_dir: Optional[str] = None
    clear_existing: bool = False


class IndexResponse(BaseModel):
    chunks_indexed: int
    message: str


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a message to the coding agent and receive a response.
    """
    try:
        response_text = await _agent.run(req.message)
        return ChatResponse(response=response_text, session_id=req.session_id or "default")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Stream the coding agent's response token-by-token (SSE).
    """
    async def event_generator():
        try:
            async for token in _agent.stream(req.message):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {e}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/index", response_model=IndexResponse)
async def index_codebase(req: IndexRequest, background_tasks: BackgroundTasks):
    """
    Trigger indexing of the codebase into the vector store.
    Runs synchronously for simplicity; move to background task for large codebases.
    """
    try:
        kwargs = {"clear_existing": req.clear_existing}
        if req.codebase_dir:
            kwargs["codebase_dir"] = req.codebase_dir

        chunks_indexed = await _retriever.index_codebase(**kwargs)
        return IndexResponse(
            chunks_indexed=chunks_indexed,
            message=f"Successfully indexed {chunks_indexed} chunks.",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memory")
async def clear_memory():
    """Clear the current conversation history."""
    _memory.clear()
    return {"message": "Conversation memory cleared."}


@router.get("/status")
async def status():
    """Return system status including index and memory stats."""
    return {
        "indexed_chunks": _vector_store.count,
        "memory_turns": _memory.turn_count,
    }
