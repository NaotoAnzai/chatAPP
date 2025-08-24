from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発中は全て許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": messages
            },
        )
    
    data = response.json()

    # choices -> message -> content を安全に取り出して返す
    assistant = None
    choices = data.get("choices")
    if isinstance(choices, list) and len(choices) > 0:
        first = choices[0]
        if isinstance(first, dict):
            msg = first.get("message")
            if isinstance(msg, dict):
                assistant = msg.get("content")

    if assistant is None:
        # 取り出せなければ元のdataをそのまま返す（デバッグ用）
        assistant = data

    return {"reply": assistant}