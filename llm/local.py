from langchain_ollama import OllamaLLM

class LLM:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2")

    def inference(self, prompt):
        answer = self.llm.invoke(prompt)
        return answer

    