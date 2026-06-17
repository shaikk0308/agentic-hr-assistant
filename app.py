import os
from dotenv import load_dotenv
load_dotenv()  # loads your .env file automatically

from typing import Optional


import asyncio
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your orchestrator
from agents.orchestrator_agent.agent import root_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session service — keeps conversation history per session
session_service = InMemorySessionService()

APP_NAME = "hr_assistant"

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Create or reuse session
    session_id = req.session_id or str(uuid.uuid4())

    try:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id="user",
            session_id=session_id
        )
    except Exception:
        session = None

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id="user",
            session_id=session_id
        )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=req.message)]
    )

    final_reply = ""

    try:
        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=user_message,
        ):
            # Only capture the final response from the orchestrator
            if (
                event.is_final_response()
                and event.author == "orchestrator_agent"
                and event.content
                and event.content.parts
            ):
                final_reply = event.content.parts[0].text or ""

        if not final_reply:
            # Fallback: grab last text from any final event
            async for event in runner.run_async(
                user_id="user",
                session_id=session_id,
                new_message=user_message,
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_reply = event.content.parts[0].text or ""

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(reply=final_reply, session_id=session_id)


@app.get("/")
async def root():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")
