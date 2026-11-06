import os 
from fastapi import FastAPI
from pydantic import BaseModel
from ai.gemini import Gemini
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from pathlib import Path

load_dotenv()

app = FastAPI()

Instrumentator().instrument(app).expose(app)

log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(exist_ok=True)
  
logger = logging.getLogger("fastapi_gemini_app")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(
        log_dir / "app.log", encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))
    logger.addHandler(handler)
logger.propagate = False

@app.middleware("http")
async def log_requests(request, call_next):
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("%s %s failed", request.method, request.url.path)
        raise
    logger.info(
        "%s %s status=%s",
        request.method, request.url.path, response.status_code
    )
    return response

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

