from app.config import DEFAULT_MODE

class Assistant():
    def __init__(self, chat_client, chat_history, pdf_agent, coding_agent):
        self.chat_client= chat_client
        self.chat_history= chat_history
        self.pdf_agent= pdf_agent
        self.coding_agent= coding_agent
        self.current_mode= DEFAULT_MODE
        self.codebase_path= "placeholder"

    def handle_request(self, request):
        if self.current_mode == "chat":
            self.chat_history.add_message("user", request)

            chat_response= self.chat_client.generate_response(self.chat_history.get_msg())

            self.chat_history.add_message("assistant", chat_response)
            return chat_response

        elif self.current_mode == "pdf":
            if self.pdf_agent is None:
                return "Please upload a PDF first."
            return self.pdf_agent.handle_request(request)
        
        elif self.current_mode == "code":
            return self.coding_agent.handle_request(request)
        
        else:
            return "Invalid Assistant Mode"

    def set_mode(self, mode):
        self.current_mode = mode
    
    def get_history(self):
        return self.chat_history.get_msg()
    
    def clear_history(self):
        self.chat_history.clear()

    def clear_pdf(self):
        self.pdf_agent = self.pdf_agent

    def set_pdf_agent(self, pdf_agent):
        self.pdf_agent = pdf_agent

    def clear_codebase(self):
        self.coding_agent = self.coding_agent
        self.set_codebase_path(None)
        
    def set_code_agent(self, code_agent):
        self.coding_agent = code_agent

    def set_codebase_path(self, path):
        self.coding_agent.set_codebase_path(path)