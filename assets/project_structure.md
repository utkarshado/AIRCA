# 📂 Project Structure

AIRA/
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
