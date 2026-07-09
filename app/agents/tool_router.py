from app.tools.read_file_tool import ReadFileTool
from app.tools.write_file_tool import WriteFileTool
from app.tools.list_files_tool import ListFilesTool
from app.tools.search_files_tool import SearchFilesTool
from app.tools.replace_text_tool import ReplaceTextTool
from app.tools.execute_python_tool import ExectuePythonTool
from app.tools.base_tool import BaseTool


class ToolRouter(BaseTool):

    def __init__(self):

        self.read_tool=ReadFileTool()
        self.write_tool=WriteFileTool()
        self.list_tool=ListFilesTool()
        self.search_tool=SearchFilesTool()
        self.replace_tool=ReplaceTextTool()
        self.execute_tool=ExectuePythonTool()

        self.functions= {
        "read_file_tool": self.read_tool.read,
        "write_file_tool": self.write_tool.write,
        "list_files_tool": self.list_tool.list,
        "search_files_tool": self.search_tool.search,
        "replace_text_tool": self.replace_tool.replace,
        "execute_python_tool": self.execute_tool.execute,
        }

    def call_tool(self, tool_name, tool_args):
 
        function= self.functions.get(tool_name)
        if function is None:
            return self.failure("Unkown tool.")
        
        return function(**tool_args)
