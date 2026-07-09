from app.tools.base_tool import BaseTool
from app.tools.read_file_tool import ReadFileTool
from app.tools.write_file_tool import WriteFileTool

class ReplaceTextTool(BaseTool):
    def replace(
            self,
            path,
            old_text,
            new_text,
    ):
        
        if not old_text:
            return self.failure("old_text cannot be empty.")
        
        read_tool= ReadFileTool()
        write_tool= WriteFileTool()
        
        read_response= read_tool.read(path)
        if not read_response["success"]:
            return self.failure(read_response["error"])
        
        content= read_response["data"]["content"]

        if old_text not in content:
            return self.failure("Provided text is not present in the file/path.")
        
        new_content= content.replace(old_text,new_text)

        write_response= write_tool.write(path, new_content)
        if not write_response["success"]:
            return self.failure(write_response["error"])
        
        data= {
            "path": path,
            "replaced": old_text,
            "replacement": new_text,
        }

        return self.success(data)
