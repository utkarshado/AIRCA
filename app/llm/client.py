from google import genai
from app.config import GEMINI_API_KEY
from ollama import chat
from app.config import OLLAMA_MODEL


class GEMINIClient:
    def __init__(self,api_key):
        self.client=genai.Client(api_key=api_key)


    def generate_response(self,history):
        response=self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history,
        )

        return response.text
    

    def rewrite_query(self, history, question):

        prompt = f"""
        Given the conversation history and current question,
        rewrite the current question so it is fully self contained.

        If the question is already complete,
        return it unchanged.

        Current Question:
        {question}
        """

        contents = []

        contents.extend(history)

        contents.append(
            {
                "role":"user",
                "parts":[{"text":prompt}]
            }
        )

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )
        )

        return response.text
    

#---------------------------------------------------------------------------------------------------------------


class OLLAMAClient:

    def generate_response(self, history):

        response = chat(
            model=OLLAMA_MODEL,
            messages=history
        )

        return response.message.content

    def rewrite_query(self, history, question):

        prompt = f"""
        Given the conversation history and current question,
        rewrite the current question so it is fully self contained.

        If the question is already complete,
        return it unchanged.

        Current Question:
        {question}
        """

        messages = history.copy()

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = chat(
            model="qwen3:14b",
            messages=messages
        )

        return response.message.content