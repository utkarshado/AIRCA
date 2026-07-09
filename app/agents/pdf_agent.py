from app.llm.prompts import PDF_AGENT_PROMPT

class PDFAgent():
    def __init__(self, client, chat_history, rag_service):
        self.client= client
        self.chat_history= chat_history
        self.pdf_rag= rag_service
    
    def handle_request(self, request):
        self.chat_history.add_message("user", request)
        messages= self._prepare_messages(request)
        response= self._call_llm(messages)
        self.chat_history.add_message("assistant", response)
        return response

    def _prepare_messages(self, request):
        messages=[]
        messages.append(
            {
                "role":"system",
                "content":PDF_AGENT_PROMPT
            }
        )
        history = self.chat_history.get_msg()
        context =self.pdf_rag.retrieve_context(request, history)
        if context:
            messages.append(
                {
                    "role":"system",
                    "content":f"Relevant Context :\n\n{context}"
                }
            )

        messages.extend(history)

        return messages     

    def _call_llm(self, messages):

        response = self.client.generate_response(messages)
        return response