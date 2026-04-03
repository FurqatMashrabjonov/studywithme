from fastapi import FastAPI
from fastapi import Depends

from app.core.exceptions import AppException
from app.dependencies.security_dependency import get_request_user
from routes.auth import router as auth_router
from routes.notebook import router as notebook_router
from routes.note import router as note_router
from app.core.exception_handlers import app_exception_handler

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(prefix="/auth", router=auth_router, tags=["Auth"])

app.include_router(
    prefix="/notebook",
    router=notebook_router,
    tags=["Notebook"],
    dependencies=[Depends(get_request_user)],
)

app.include_router(
    prefix="/{notebook_uid}/note",
    router=note_router,
    tags=["Note"],
    dependencies=[Depends(get_request_user)],
)









#------------------------------------------------------------------


import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from pydantic import BaseModel

load_dotenv()

# --- DB ---
DB_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_DATABASE')}"
)

session_service = DatabaseSessionService(db_url=DB_URL)

# --- Agent ---
root_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    instruction="Sen foydali assistantsan. Savollarga aniq va qisqa javob ber.",
)

# --- Compaction ---
summarizer = LlmEventSummarizer(llm=Gemini(model="gemini-2.0-flash"))

adk_app = App(
    name="my_app",
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=10,  # har 10 turn da compress qiladi
        overlap_size=2,          # oxirgi 2 turn saqlanib qoladi
        summarizer=summarizer,
    ),
)

# --- Runner ---
runner = Runner(
    agent=root_agent,
    app_name="my_app",
    session_service=session_service,
)


# --- API ---
class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    # session yo'q bo'lsa yangi ochadi, bor bo'lsa topadi
    existing = await session_service.list_sessions(
        app_name="my_app", user_id=req.user_id
    )

    if existing and existing.sessions:
        session_id = existing.sessions[0].id
    else:
        session = await session_service.create_session(
            app_name="my_app", user_id=req.user_id
        )
        session_id = session.id

    content = types.Content(role="user", parts=[types.Part(text=req.message)])

    response_text = ""
    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response_text = event.content.parts[0].text

    return {"response": response_text, "session_id": session_id}