import os 
from fastapi import FastAPI
from pydantic import BaseModel
from ai.gemini import Gemini
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

def load_system_prompt():
      with open("ai/prompts/system_prompt.md","r") as f:
            return f.read()

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

class ChatRequest(BaseModel):
    prompt: str #expects JSON

class ChatResponse(BaseModel):
    response: str #returns JSON


# api endpoints-
@app.get('/')
def root():
         return "API is running"

@app.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest):
      response_text=ai_platform.chat(request.prompt)
      return ChatResponse(response = response_text)

