from app.tools.base_tool import BaseTool
import os

class WriteFileTool(BaseTool):

    def write(self, path, content):
        directory= os.path.dirname(path)
        if not os.path.isdir(directory):
            return self.failure("Directory does not exist.")
        
        try:
            with open(path, "w", encoding="utf-8", errors="ignore")as f:
                f.write(content)
            
        except Exception as e:
            return self.failure(str(e))

        data= {
            "path":path,
            "characters": len(content)
        }

        return self.success(data)















































"""
tools/write_file.py - Tool that writes or overwrites a file in the codebase.


from pathlib import Path
from app.config import settings


class WriteFileTool:
    ##Writes content to a file, creating parent directories as needed.##

    def definition(self) -> dict:
        return {
            "name": "write_file",
            "description": (
                "Write content to a file in the codebase. "
                "Creates the file (and parent directories) if they do not exist. "
                "Always read the file first if it already exists."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file (e.g. 'src/utils.py').",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full file content to write.",
                    },
                },
                "required": ["path", "content"],
            },
        }

    async def run(self, path: str, content: str) -> str:
        
        ##Write content to a file.

        Args:
            path:    Relative path inside the codebase directory.
            content: Full content to write (overwrites existing file).

        Returns:
            Success message or error string.
        ##
        base = Path(settings.CODEBASE_DIR).resolve()
        target = (base / path).resolve()

        # Prevent path traversal
        if not str(target).startswith(str(base)):
            return f"Error: Access denied — '{path}' is outside the codebase directory."

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return f"Successfully wrote {len(content)} characters to '{path}'."
        except Exception as e:
            return f"Error writing file: {e}

"""
