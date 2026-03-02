from ollama import chat

class LLM:
    def __init__(self):
        self.model = "ministral-3"

    def inference(self, prompt):
        response = chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.message.content

    
