import os
from app.tools.base_tool import BaseTool

class ReadFileTool(BaseTool):

    def read(self, path):

        if not os.path.exists(path):
            return self.failure("Path does not exist.")

        if not os.path.isfile(path):
            return self.failure("Path is not a file.")
        
        try:
            with open(path,"r",encoding="utf-8",errors="ignore")as f:
                contents= f.read()
        except Exception as e:
            return self.failure(str(e))
            
        data= {
            "path": path,
            "content": contents,
            "characters":len(contents),
        }
        return self.success(data)
        