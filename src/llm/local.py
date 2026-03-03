from ollama import chat

class LLM:
    def __init__(self):
        self.model = "ministral-3"

    def inference(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        response = chat(
            model=self.model,
            messages=messages,
        )
        return response.message.content

    
