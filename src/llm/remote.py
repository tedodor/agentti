import torch
from transformers import Mistral3ForConditionalGeneration, MistralCommonBackend
import requests
import os
class LLM:
    # Remote inference function using Hugging Face Inference API
    def inference(self, prompt, model="gpt2", api_key=None):
        """
        Sends a prompt to a remote Hugging Face model and returns the response.
        Args:
            prompt (str): The input prompt for the model.
            model (str): The model ID on Hugging Face Hub (default: 'gpt2').
            api_key (str): Your Hugging Face API key. If None, reads from HF_API_KEY env variable.
        Returns:
            str: The model's response.
        """
        if api_key is None:
            api_key = os.getenv("HF_API_KEY")
        if not api_key:
            raise ValueError("Hugging Face API key not provided. Set HF_API_KEY env variable or pass as argument.")
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # For text generation models, result is usually a list of dicts with 'generated_text'
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        return str(result)
