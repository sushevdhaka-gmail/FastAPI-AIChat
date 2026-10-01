import os
from google import genai
from google.genai import types
from .base import AIPlatform

class Gemini(AIPlatform):
    def __init__(self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client=genai.Client(api_key=api_key)
        self.model_name = "gemini-3.1-flash-lite"

    def chat(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt
            ) if self.system_prompt else None
        )
        return response.text