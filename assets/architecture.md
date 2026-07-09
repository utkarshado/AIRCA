LLM          = Ollama (Qwen3-14B)
RAG          = Retrieval-Augmented Generation
Workspace    = Local Folder / ZIP / GitHub Repo

---------------------------------------------------------------------------------------------------
# PROJECT WORKFLOW
 
 
                                      User
                                        │
                                        │
                           Streamlit Web Interface
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
      Chat Mode                     PDF Mode                     Code Mode
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │                             
                                    Assistant Router (Assistant.py)
                                        │
                     ┌──────────────────┼──────────────────┐
                     │                  │                  │
                 General Chat       PDF Agent          Coding Agent
                     │                  │                  │
                     │             PDF RAG            Code RAG
                     │                  │                  │
                     │        Semantic Retrieval   Semantic Retrieval
                     │                  │                  │
                     └──────────────────┼──────────────────┘
                                        │
                                    Ollama Client
                                    (Qwen3-14B)
                                        │
                                Generated Response
                                        │
                                    Streamlit UI

---------------------------------------------------------------------------------------------------                 
# WORKSPACE MANAGER

                 User
                   │
          Streamlit Interface
                   │
          Assistant Router
                   │
        ┌──────────┴──────────┐
        │                     │
     Chat Mode           Knowledge Sources
                              │
      ┌───────────────┬───────────────┬───────────────┐
      │               │               │               |
   PDF Upload     Local Folder    ZIP Upload     GitHub Repo       
      │               │               │               |
      └───────────────┴───────────────┴───────────────┘
                              │
                       Workspace Manager
                              │
                    PDF Agent / Code Agent

                    
---------------------------------------------------------------------------------------------------

# PDF RAG WORKFLOW

                Uploaded PDF
                     │
                     ▼
             PDF Loader (PyMuPDF)
                     │
                     ▼
              PDF Chunker
                     │
                     ▼
        Sentence Transformer Embeddings
                     │
                     ▼
              Vector Store (.pkl)
                     │
──────────────── User Question ────────────────
                     │
                     ▼
           Semantic Retriever (Top-K)
                     │
                     ▼
          Retrieved Relevant Chunks
                     │
                     ▼
             Ollama (Qwen3-14B)
                     │
                     ▼
            Context-Aware Answer

---------------------------------------------------------------------------------------------------

# CODE RAG WORKFLOW

          Local Folder / ZIP / GitHub Repo
                        │
                        ▼
                 Code Loader
                        │
                        ▼
            AST Code Chunker (Python)
                        │
                        ▼
     Sentence Transformer Embeddings
                        │
                        ▼
              Code Vector Store
                        │
────────────── User Query ───────────────
                        │
                        ▼
            Semantic Code Retriever
                        │
                        ▼
          Relevant Code Chunks
                        │
                        ▼
                Coding Agent
                        │
         ┌──────────────┴───────────────┐
         │                              │
     Needs Tool?                    Direct Answer
         │                              │
         ▼                              ▼
     Tool Router                  Ollama LLM
         │                              │
         ▼                              ▼
 Execute Tool(s)                 Final Response
         │
         ▼
 Tool Result → LLM → Final Response

---------------------------------------------------------------------------------------------------

# TOOL CALLING WORKFLOW

           User Request
                │
                ▼
         Coding Agent
                │
                ▼
     Build Prompt + Workspace
                │
                ▼
          Ollama LLM
                │
      ┌─────────┴─────────┐
      │                   │
 No Tool Call       Tool Call JSON
      │                   │
      ▼                   ▼
 Return Answer      Tool Router
                          │
     ┌──────────────┬──────────────┬─────────────┬──────────────┬──────────────┐
     │              │              │             │              |              |
 Read File      Write File    Search File     List File    Replace File   Execute Python
     │              │              │             │              |              |
     └──────────────┴──────────────┴─────────────┴──────────────┴──────────────┘
                          │
                          ▼
                   Tool Result
                          │
                          ▼
                    Ollama Again
                          │
                          ▼
                    Final Answer


