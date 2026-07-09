from app.agents.tool_router import ToolRouter
from app.llm.prompts import CODING_AGENT_PROMPT
import json
from app.config import VALID_TOOL_NAMES,MAX_TOOL_CALLS

class CodingAgent():
    def __init__(self, client, chat_history, rag_service):
        self.client= client
        self.tool_router= ToolRouter()
        self.chat_history= chat_history
        self.code_rag= rag_service
        self.codebase_path = None

    def handle_request(self, request):
        self.chat_history.add_message("user", request)
        for _ in range(MAX_TOOL_CALLS):

            messages= self._prepare_messages(request)
            response= self._call_llm(messages)
            tool_call= self._parse_tool_call(response)

            if tool_call is None:
                self.chat_history.add_message("assistant", response)
                return response
            
            tool_result= self._execute_tool(tool_call)
            self._append_tool_result(tool_result)

        return "Maximum tool calls exceeded."
    
    def set_codebase_path(self, path):
        self.codebase_path = path

    def _prepare_messages(self, request):
        messages=[]
        messages.append(
            {
                "role":"system",
                "content":CODING_AGENT_PROMPT
            }
        )
        messages.append(
            {
                "role":"system",
                "content":f"WORKSPACE_ROOT: {self.codebase_path}"
            }
        )
        history = self.chat_history.get_msg()
        context =self.code_rag.retrieve_context(request, history)
        if context.strip():
            messages.append(
                {
                    "role":"system",
                    "content":f"Relevant Project Context :\n\n{context}"
                }
            )

        messages.extend(history)

        return messages
    
    def _call_llm(self, messages):
        response= self.client.generate_response(messages)
        return response

        
    def _parse_tool_call(self, response):
        try:  
                tool_call=json.loads(response)
        except json.JSONDecodeError as e:
            return None
        tool_name= tool_call.get("tool")
        if tool_name not in VALID_TOOL_NAMES:
            return None
        if not isinstance(tool_call["arguments"], dict):
            return None
        return tool_call
        
    def _execute_tool(self, tool_call):
        tool_name = tool_call["tool"]
        tool_args = tool_call["arguments"]
        tool_result= self.tool_router.call_tool(tool_name, tool_args)
        return tool_result
    
    def _format_tool_result(self, tool_result):
        return json.dumps(tool_result, indent=2)

    def _append_tool_result(self, tool_result):
        formatted_tool_result= self._format_tool_result(tool_result)
        self.chat_history.add_message("tool", formatted_tool_result)
        
         
