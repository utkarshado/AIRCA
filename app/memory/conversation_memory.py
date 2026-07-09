import os
import json
from app.config import history_path



class ChatHistory:

    def __init__(self):
        self.messages = []
        self.load()

    def load(self):
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                self.messages = json.load(f)

    def save(self):
        with open(history_path, "w") as f:
            json.dump(self.messages, f, indent=4)

    def add_message(self, role, text):
        self.messages.append(
            {
                "role": role,
                "content": text
            }
        )
        self.save()
    #change this to get_messages
    def get_msg(self):
        return self.messages
    #change this to print_history or get_history
    def list(self):
        print("HISTORY--------------------------------------------\n")

        for msg in self.messages:
            if msg["role"] == "user":
                print(f"YOU      : {msg['content']}")

            elif msg["role"] == "assistant":
                print(f"ASSISTANT: {msg['content']}")

            elif msg["role"] == "tool":
                print(f"TOOL     : {msg['content']}")

    def clear(self):
        self.messages = []
        self.save()

    
    def get_history_text(self):

        history = ""

        for msg in self.messages:
            if msg["role"].lower() == "user":
                history += f"User: {msg['content']}\n"
            elif msg["role"].lower() == "assistant":
                history += f"Assistant: {msg['content']}\n"
            elif msg["role"].lower() == "tool":
                history += f"Tool: {msg['content']}\n"
        return history

