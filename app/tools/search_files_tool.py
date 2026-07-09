from app.tools.base_tool import BaseTool
from app.tools.read_file_tool import ReadFileTool
from app.tools.list_files_tool import ListFilesTool


class SearchFilesTool(BaseTool):

    def search(self, path, query):

        results= []
        list_tool= ListFilesTool()
        read_tool= ReadFileTool()

        list_response= list_tool.list(path)
        if not list_response["success"]:
            return self.failure(list_response["error"])

        for file in list_response["data"]:
            read_response= read_tool.read(file["path"])
            if not read_response["success"]:
                continue

            if query.lower() in read_response["data"]["content"].lower():
                results.append(
                    {
                    "name": file["name"],
                    "path": file["path"]
                    }
                )

        return self.success(results)


