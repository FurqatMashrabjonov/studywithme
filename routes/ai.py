from fastapi import APIRouter
from dotenv import load_dotenv
from fastapi import Depends
from google.adk.agents import Agent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from google.adk.planners import BuiltInPlanner
from pydantic import BaseModel

from app.dependencies.route_dependency import get_valid_notebook
from app.dependencies.security_dependency import get_request_user
from app.models import User, Notebook
from app.core.config import settings

load_dotenv()
router = APIRouter()

session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)

root_agent = Agent(
    name="Girgitton",
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #         thinking_budget=1024,
    #     )
    # ),
    model="gemini-3.1-flash-lite-preview",
    instruction="Sen 'Girgitton ismli ta'lim olishda yordamchi agentsan. Foydalanuvchiga bir mavzuni o'rganishi uchun yordam berasan.'",
)

adk_app = App(
    name="my_app",
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=10,  # har 10 turn da compress qiladi
        overlap_size=2,          # oxirgi 2 turn saqlanib qoladi
        summarizer=LlmEventSummarizer(llm=Gemini(model="gemini-2.0-flash")),
    ),
)

runner = Runner(
    agent=root_agent,
    app_name="my_app",
    session_service=session_service,
    auto_create_session=True,
)

class TokenUsage(BaseModel):
    input: int
    output: int
    total: int

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(
        req: ChatRequest,
        user: User = Depends(get_request_user),
        notebook: Notebook = Depends(get_valid_notebook)
):
    session_id = str(notebook.uid)
    user_id_str = str(user.id)
    content = types.Content(role="user", parts=[types.Part(text=req.message)])
    response_text = ""
    token_usage = {}

    async for event in runner.run_async(
        user_id=user_id_str,
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts and event.content.parts[0].text:
            response_text = event.content.parts[0].text
            token_usage = TokenUsage(
                input=event.usage_metadata.prompt_token_count,
                output=event.usage_metadata.candidates_token_count,
                total=event.usage_metadata.total_token_count,
            )

    return {
        "response": response_text,
        "session_id": session_id,
        "token_usage": token_usage
    }