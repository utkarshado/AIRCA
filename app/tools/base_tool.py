class BaseTool:

    def success(self, data):
        return {
            "success": True,
            "data": data
        }


    def failure(self, error):
        return {
            "success": False,
            "error": error
        }