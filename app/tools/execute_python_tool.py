from app.tools.base_tool import BaseTool
import os
import sys
import subprocess

class ExectuePythonTool(BaseTool):
    def execute(self, path):

        if not os.path.exists(path):
            return self.failure("Path does not exist.")
        
        if not os.path.isfile(path):
            return self.failure("Path is not a file.")
        
        extension= os.path.splitext(path)[1]
        if extension != ".py":
            return self.failure("Not a python file.")
        
        try:
            result= subprocess.run([sys.executable(), path], capture_output= True, text=True, timeout=7)
            output= result.stdout.strip()
            error= result.stderr.strip()

        except subprocess.TimeoutExpired:
            return self.failure("Execution timed out after 7 seconds.")
        except Exception as e:
            return self.failure(str(e))
        


        data={
            "path": path,
            "stdout": output,
            "stderr": error,
            "return_code": result.returncode
        }

        return self.success(data)