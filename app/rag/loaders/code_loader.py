import os
from app.config import valid_extensions
from app.config import ignored_directories

class CodeLoader():

    def load(self,project_path):
        code=[]

        for root,dirs,files in os.walk(project_path):
            
            dirs[:]=[d for d in dirs if d not in ignored_directories]

            for fil in files:
                path=os.path.join(root, fil)
                if os.path.splitext(fil)[1] in valid_extensions:
                    with open(path,"r",encoding="utf-8",errors="ignore")as f:
                        content=f.read()
                        code.append(
                            {
                                "path":path,
                                "content":content
                            }
                        )

        return code