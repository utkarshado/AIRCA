#python -m streamlit run app/frontend/streamlit_app.py
import streamlit as st
import stat
import os
import tempfile
import zipfile
import shutil
import subprocess
from app.config import (
    PDF_PATH,
    PDF_STORE,
    CODEBASE_PATH,
    CODEBASE_STORE
)
# LLM
from app.llm.client import OLLAMAClient
from app.memory.conversation_memory import ChatHistory
# PDF
from app.rag.ingestion import PDFIngestor
from app.rag.rag_service import PDFRAGService
from app.agents.pdf_agent import PDFAgent
# Code
from app.rag.ingestion import CodeIngestor
from app.rag.rag_service import CODERAGService
from app.agents.coding_agent import CodingAgent
# Assistant
from app.agents.assistant import Assistant

def initialize_assistant():
    client = OLLAMAClient()
    history = ChatHistory()

    pdf_ingestor=PDFIngestor()
    pdf_vector_store= pdf_ingestor.ingest(PDF_PATH, PDF_STORE)
    pdf_rag= PDFRAGService(pdf_vector_store)
    pdf_agent= PDFAgent(client, history, pdf_rag)

    code_ingestor= CodeIngestor()
    code_vector_store= code_ingestor.ingest(CODEBASE_PATH, CODEBASE_STORE) 
    code_rag= CODERAGService(code_vector_store)
    code_agent= CodingAgent(client, history, code_rag)

    assistant= Assistant(client, history, pdf_agent, code_agent)
    return assistant

def load_codebase(path, store):

    code_ingestor = CodeIngestor()

    code_vector_store = code_ingestor.ingest(
        path,
        store
    )
    code_rag = CODERAGService(
        code_vector_store
    )
    code_agent = CodingAgent(
        assistant.chat_client,
        assistant.chat_history,
        code_rag
    )
    assistant.set_code_agent(
        code_agent
    )

    assistant.set_codebase_path(
        path
    )


def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


#--------------------------------------------------------------------------------------------------------

if "assistant" not in st.session_state:
    st.session_state.assistant = initialize_assistant()

#backgroiund and style

st.markdown("""
<style>

/* Wallpaper */
.stApp {
    background-image: url("https://c4.wallpaperflare.com/wallpaper/698/917/306/minimalism-simple-blue-gradient-wallpaper-preview.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Top bar */
[data-testid="stHeader"] {
    background: rgba(10,15,30,0.85);
    backdrop-filter: blur(15px);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15,20,35,0.90);
    backdrop-filter: blur(20px);
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(15,20,35,0.90);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
}

/* Info boxes */
[data-testid="stAlert"] {
    background: rgba(20,40,80,0.65);
    border-radius: 12px;
}

/* Optional */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)



# interface
st.set_page_config(
    page_title="AI Research & Intelligence Assistant",
    layout="wide"
)

st.title("🍹 A.I.R.A.")
st.subheader("AI Research & Intelligence Assistant")
st.caption(" • General Chat  • PDF Q&A  • Cursor-style Coding Assistant")


# sidebar
with st.sidebar:

    st.header("Mode")

    mode = st.radio(
        "Choose Assistant Mode",
        ["Chat", "PDF", "Code"]
    )
assistant = st.session_state.assistant
assistant.set_mode(mode.lower())
# mode badge
st.divider()

mode_icons = {
    "Chat": "💬",
    "PDF": "📄",
    "Code": "💻"
}

st.info(
    f"Current Mode : {mode_icons[mode]} **{mode}**"
)

st.divider()
st.subheader("Knowledge Sources")

# pdf mode ------------------------------------------------------------------
if mode == "PDF":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = None

    if (
    uploaded_pdf is not None
    and uploaded_pdf.name != st.session_state.pdf_name
    ):
        pdf_store = os.path.join(
                tempfile.gettempdir(),
                "uploaded_pdf_store.pkl"
            )
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_pdf.getbuffer())
            temp_pdf_path = temp_file.name

        try:
            with st.spinner("Indexing PDF..."):
                pdf_ingestor = PDFIngestor()

                pdf_vector_store = pdf_ingestor.ingest(
                    temp_pdf_path,
                    pdf_store
                )

                pdf_rag = PDFRAGService(
                    pdf_vector_store
                )

                pdf_agent = PDFAgent(
                    assistant.chat_client,
                    assistant.chat_history,
                    pdf_rag
                )

                assistant.set_pdf_agent(pdf_agent)
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

        st.session_state.pdf_name = uploaded_pdf.name
        st.success(f"{uploaded_pdf.name} indexed successfully!")
        st.session_state.pdf_store = pdf_store

    if st.session_state.pdf_name is not None:
        st.info(f"📄 Current PDF: {st.session_state.pdf_name}")
        if st.button("🗑 Remove PDF"):

            assistant.clear_pdf()

            if (
                st.session_state.pdf_store
                and os.path.exists(st.session_state.pdf_store)
            ):
                os.remove(st.session_state.pdf_store)

            st.session_state.pdf_name = None
            st.session_state.pdf_store = None

            st.success("PDF removed.")
            st.rerun()
#-----------------------------------------------------------------------------------------------

if mode == "Code":

    source = st.radio(
        "Choose Code Source",
        [
            "📁 Local Folder",
            "📦 ZIP Repository",
            "🌐 GitHub Repository"
        ]
    )

    workspace_store = os.path.join(
        tempfile.gettempdir(),
        "uploaded_code_store.pkl"
    )   

# code mode (local path)----------------------------------------------------------------------

    if source == "📁 Local Folder":
        codebase_path = st.text_input(
            "Project Folder",
            placeholder=r"C:\Users\Utkarsh\Desktop\my_project"
        )
        index_code = st.button("📂 Index Codebase")

        if "workspace_path" not in st.session_state:
            st.session_state.workspace_path = None

        if (
            index_code
            and codebase_path != st.session_state.workspace_path
        ):

            if not os.path.exists(codebase_path):
                st.error("Folder does not exist.")

            elif not os.path.isdir(codebase_path):
                st.error("Please enter a folder path.")

            else:
                with st.spinner("Indexing Codebase..."):
                    load_codebase(codebase_path, workspace_store)
                    st.success("✅ Codebase indexed successfully!")
                    st.session_state.workspace_path = codebase_path
                    st.session_state.workspace_name = os.path.basename(codebase_path)
                    st.session_state.workspace_type = "local"
                    st.session_state.workspace_store = workspace_store
                    st.session_state.workspace_icon = "📁"

# code mode (zip deployment)------------------------------------------------------

    elif source == "📦 ZIP Repository":
        uploaded_zip = st.file_uploader(
            "Upload ZIP Repository",
            type=["zip"]
        )
        index_code = st.button("📦 Index Codebase")
        if "workspace_path" not in st.session_state:
            st.session_state.workspace_path = None

        if (uploaded_zip is not None
            and index_code
            and uploaded_zip.name != st.session_state.get("workspace_name")
        ):
            
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".zip"
            ) as temp_zip:
                temp_zip.write(uploaded_zip.getbuffer())
                zip_path = temp_zip.name
            
            extract_dir = tempfile.mkdtemp()

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            if not os.path.exists(extract_dir):
                st.error("Folder does not exist.")

            elif not os.path.isdir(extract_dir):
                st.error("Please enter a folder path.")

            else:
                with st.spinner("Indexing Codebase..."):
                    load_codebase(extract_dir, workspace_store)
                    st.success("✅ Codebase indexed successfully!")
                    st.session_state.workspace_path = extract_dir
                    st.session_state.workspace_name = uploaded_zip.name
                    st.session_state.workspace_type = "zip"
                    st.session_state.workspace_store = workspace_store
                    st.session_state.workspace_icon = "📦"
                    os.remove(zip_path)

# code mode (github repo deployment)------------------------------------------------------

    elif source == "🌐 GitHub Repository":

        repo_url = st.text_input("Repository URL")
        index_repo = st.button("🌐 Clone & Index")

        if index_repo and repo_url:

            old_workspace = st.session_state.get("workspace_path")

            if (
                old_workspace
                and st.session_state.get("workspace_type") == "zip"
                and os.path.exists(old_workspace)
            ):
                shutil.rmtree(old_workspace)

            clone_dir = tempfile.mkdtemp()

            try:
                subprocess.run(
                    ["git", "clone", repo_url, clone_dir],
                    check=True
                )
            except subprocess.CalledProcessError:
                st.error("Failed to clone repository.")
                st.stop()
            with st.spinner("Indexing Codebase..."):
                load_codebase(clone_dir, workspace_store)

                assistant.set_codebase_path(clone_dir)

                st.success("✅ Repository indexed successfully!")
                st.session_state.workspace_path = clone_dir
                st.session_state.workspace_name = repo_url.split("/")[-1]
                st.session_state.workspace_type = "github"
                st.session_state.workspace_store = workspace_store
                st.session_state.workspace_icon = "🌐"


#-----------------------------------------------------------------------------------------

    st.divider()
    if st.session_state.get("workspace_name"):

        st.info(
        f"""
### {st.session_state.workspace_icon} Current Workspace

**Name:** {st.session_state.workspace_name}

**Source:** {st.session_state.workspace_type.title()}
"""
        )

        if st.button("🗑 Remove Workspace"):

            assistant.clear_codebase()

            if (
                st.session_state.workspace_type in ["zip", "github"]
                and os.path.exists(st.session_state.workspace_path)
            ):
                shutil.rmtree(
                    st.session_state.workspace_path,
                    onerror=remove_readonly
                )

            if os.path.exists(st.session_state.workspace_store):
                os.remove(st.session_state.workspace_store)

            st.session_state.workspace_path = None
            st.session_state.workspace_name = None
            st.session_state.workspace_type = None
            st.session_state.workspace_store = None

            st.success("Workspace removed.")
            st.rerun()


# history ------------------------------------------------------------------------
history = assistant.get_history()

avatars = {
    "user": "🗽",
    "assistant": "🧠",
    "tool": "🛠️"
}

for message in history:
    with st.chat_message(
        message["role"],
        avatar=avatars[message["role"]]
    ):
        st.markdown(message["content"])

if st.button("🗑️ Clear Chat"):
    assistant.clear_history()
    st.rerun()


# input
user_input = st.chat_input("Ask anything...")

if user_input:
    with st.chat_message(
        "user",
        avatar=avatars["user"]
    ):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        response = assistant.handle_request(user_input)

    with st.chat_message(
        "assistant",
        avatar=avatars["assistant"]
    ):
        st.markdown(response)

    st.rerun()
#------------------------------------------------------------------------------

