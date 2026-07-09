# 🍹 A.I.R.C.A. — AI Research & Coding Assistant

A.I.R.C.A. is a Cursor-inspired AI engineering assistant that combines **General Chat**, **PDF Question Answering**, and **Codebase Understanding** into a single application.

Built using **Python**, **Streamlit**, **Ollama**, **Qwen3-14B**, **Sentence Transformers**, and a custom Retrieval-Augmented Generation (RAG) pipeline.

---------------------------------------------------------------------

# ✨ Features

## 💬 General Chat
- Multi-turn conversation
- Persistent conversation history
- Local LLM (Qwen3-14B via Ollama)
- Fast responses without cloud APIs

---------------------------------------------------------------------

## 📄 PDF Assistant

Upload any PDF and ask questions about its contents.

Features:

- Automatic PDF ingestion
- Semantic chunking
- Sentence Transformer embeddings
- Vector search
- Context-aware RAG responses
- Multi-turn conversations grounded in the uploaded document

---------------------------------------------------------------------

## 💻 Cursor-style Coding Assistant

Analyze an entire codebase using natural language.

Supports:

- Local project folders
- ZIP repositories
- GitHub repositories

Capabilities:

- Understand project architecture
- Explain functions and classes
- Navigate large codebases
- Retrieve relevant files using semantic search
- Tool-calling for filesystem operations

---------------------------------------------------------------------

## 🧠 Tool Calling

The coding assistant can intelligently use tools instead of relying solely on the language model.

Current tools include:

- Read File
- Write File
- Search Files
- List Files
- Execute Python Code

---------------------------------------------------------------------

## 🗂 Workspace Management

Supports switching between multiple workspaces.

Workspace sources:

- Local Folder
- ZIP Repository
- GitHub Repository

Each workspace is independently indexed for semantic retrieval.

---------------------------------------------------------------------

## 🧠 Retrieval-Augmented Generation (RAG)

Both the PDF assistant and coding assistant use RAG.

Pipeline:

Document / Code
        ↓
Chunking
        ↓
Sentence Transformer Embeddings
        ↓
Vector Store
        ↓
Semantic Retrieval
        ↓
Local LLM
        ↓
Grounded Response

---------------------------------------------------------------------

# 🏗 Architecture

assets/architecture.md

---------------------------------------------------------------------

# 🛠 Tech Stack

## Language

- Python

## Frontend

- Streamlit

## LLM

- Ollama
- Qwen3-14B

## Embeddings

- Sentence Transformers

## PDF Processing

- PyMuPDF

## Vector Search

- ChromaDB / Custom Vector Store

## Backend

- FastAPI
- Uvicorn

---------------------------------------------------------------------

# 📂 Project Structure
```
AIRCA/
│
├── app/
│   ├── agents/
│   │   ├── assistant.py
│   │   ├── coding_agent.py
│   │   ├── pdf_agent.py
│   │   └── tool_router.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── frontend/
│   │   └── streamlit_app.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   └── prompts.py
│   │
│   ├── memory/
│   │   ├── conversation_memory.py
│   │   └── history.json
│   │
│   ├── rag/
│   │   ├── chunkers/
│   │   ├── loaders/
│   │   ├── embedder.py
│   │   ├── ingestion.py
│   │   ├── rag_service.py
│   │   ├── retriever.py
│   │   └── vector_store.py
|   |
│   ├── storage/
│   │   ├── pdf_vectore_store.pkl
│   │   └── code_vectore_store.pkl
|   |
│   ├── tools/
│   │   ├── base_tool.py
│   │   ├── execute_python_tool.py
│   │   ├── list_files_tool.py
│   │   ├── read_file_tool.py
│   │   ├── replace_text_tool.py
│   │   ├── search_files_tool.py
│   │   └── write_file_tool.py
│   │
│   ├── config.py
│   └── main.py
│
├── assets/
│   ├── demo.gif
│   ├── architecture.md
│   └── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore
```
Note: The api/ module is reserved for future FastAPI deployment. The current version runs through a Streamlit interface.
---------------------------------------------------------------------

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/utkarshado/AIRCA-clone.git
```

Move into the project

```bash
cd cursor-clone
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---------------------------------------------------------------------

# ⚙️ Run Ollama

Start Ollama

```bash
ollama serve
```

Download the model

```bash
ollama pull qwen3:14b
```

---------------------------------------------------------------------

# ▶️ Launch the Application

```bash
streamlit run app/frontend/streamlit_app.py
```

---------------------------------------------------------------------

# 📌 Current Capabilities

- General AI Chat
- PDF RAG
- Code RAG
- Semantic Retrieval
- AST-based Code Chunking
- Conversation Memory
- Tool Calling
- Local LLM Inference
- Local Folder Indexing
- ZIP Repository Indexing
- GitHub Repository Indexing
- Workspace Management

---------------------------------------------------------------------

# 🔮 Planned Improvements

- Multi-Agent Software Engineering Team
- Hybrid Search (BM25 + Dense Retrieval)
- Cross-Repository Search
- Streaming Responses
- Syntax Highlighting
- Docker Support
- Deployment
- MCP Integration
- Agent Planning
- Repository Summarization

---------------------------------------------------------------------

# 👨‍💻 Author

**Utkarsh Mishra**


GitHub:
https://github.com/utkarshado

LinkedIn:
https://www.linkedin.com/in/utkarsh-mishra-ml74/

---------------------------------------------------------------------

# ⭐ If you found this project useful

Please consider giving the repository a star ⭐
