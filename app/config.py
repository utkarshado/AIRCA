from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

OLLAMA_MODEL="qwen3:14b"
#OLLAMA_MODEL="qwen2.5-coder:14b"

history_path= r"C:\Users\utkar\Downloads\ai_engineering\cursor_assistant\AIRA\app\memory\history.json"


PDF_PATH= r"C:\Users\utkar\Downloads\material\attention_is_all_you_need.pdf"
PDF_STORE= r"C:\Users\utkar\Downloads\ai_engineering\cursor_assistant\AIRA\app\storage\pdf_vector_store.pkl"

CODEBASE_PATH= r"C:\Users\utkar\Downloads\ai_engineering\simple_python_project"
CODEBASE_STORE= r"C:\Users\utkar\Downloads\ai_engineering\cursor_assistant\AIRA\app\storage\code_vector_store.pkl"

valid_extensions={".py",
                    ".js",
                    ".ts",
                    ".java",
                    ".cpp",
                    ".c",
                    ".h",
                    }

ignored_directories={"__pycache__",
                    ".git",
                    ".venv", 
                    "venv", 
                    "node_modules", 
                    "dist", 
                    "build"
                    }

AVAILABLE_TOOLS = """
read_file_tool(path)
write_file_tool(path, content)
list_files_tool(path)
search_files_tool(path, query)
replace_text_tool(path, old_text, new_text)
execute_python_tool(path)
"""

VALID_TOOL_NAMES = {
    "read_file_tool",
    "write_file_tool",
    "list_files_tool",
    "search_files_tool",
    "replace_text_tool",
    "execute_python_tool",
}

MAX_TOOL_CALLS=10

DEFAULT_MODE="chat"

