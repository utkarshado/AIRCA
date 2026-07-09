from app.config import valid_extensions
from app.config import ignored_directories
from app.tools.base_tool import BaseTool
import os

class ListFilesTool(BaseTool):

    def list(self, path):

        if not os.path.exists(path):
            return self.failure("Path does not exist.")
        
        if not os.path.isdir(path):
            return self.failure("Path is not a directory.")

        file_list= []
        try:
            for root, dirs, files in os.walk(path):
                dirs[:]=[d for d in dirs if d not in ignored_directories]
                for file in files:

                    if os.path.splitext(file)[1] in valid_extensions:
                        file_list.append({
                            "name": file,
                            "path": os.path.join(root, file)
                        })

        except Exception as e:
            return self.failure(str(e))
        
        return self.success(file_list)

               














































"""
tools/list_files.py - Lists files and directories inside the codebase.

from pathlib import Path
from typing import Optional

from app.config import settings


class ListFilesTool:
    ##Directory listing tool for the codebase.##

    def definition(self) -> dict:
        return {
            "name": "list_files",
            "description": (
                "List files and directories in the codebase. "
                "Use this to explore the project structure before reading or editing files."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": (
                            "Relative path of the directory to list. "
                            "Defaults to the root of the codebase."
                        ),
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to list files recursively (default false).",
                    },
                },
                "required": [],
            },
        }

    async def run(self, directory: str = ".", recursive: bool = False) -> str:
        ##
        List the contents of a directory.

        Args:
            directory: Relative path to list.
            recursive: Whether to recurse into subdirectories.

        Returns:
            Formatted directory tree string.
        ##
        base = Path(settings.CODEBASE_DIR).resolve()
        target = (base / directory).resolve()

        if not str(target).startswith(str(base)):
            return "Error: Access denied — path is outside the codebase directory."

        if not target.exists():
            return f"Error: Directory not found — '{directory}'."

        if not target.is_dir():
            return f"Error: '{directory}' is a file, not a directory."

        entries = []
        if recursive:
            for path in sorted(target.rglob("*")):
                rel = path.relative_to(base)
                prefix = "  " * (len(rel.parts) - 1)
                entries.append(f"{prefix}{'📁 ' if path.is_dir() else '📄 '}{path.name}")
        else:
            for path in sorted(target.iterdir()):
                icon = "📁 " if path.is_dir() else "📄 "
                entries.append(f"{icon}{path.name}")

        if not entries:
            return f"Directory '{directory}' is empty."

        header = f"Contents of '{directory}' ({len(entries)} items):"
        return header + "\n" + "\n".join(entries)
        
"""