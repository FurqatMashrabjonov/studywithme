from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from app.ai.agents.root_agent import RootAgent
from app.core.config import settings
from app.schemes.ai_scheme import StateDelta, AiStreamResponse

session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)
root_agent = RootAgent().get_agent()
app = App(
    name="my_app",
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=10,
        overlap_size=2,
        summarizer=LlmEventSummarizer(llm=Gemini(model="gemini-2.0-flash")),
    ),
)


class Orchestrator:
    def __init__(self, user_id: str, session_id: str):
        self.user_id = user_id
        self.session_id = session_id

        self._runner = Runner(
            agent=root_agent,
            app_name="my_app",
            session_service=session_service,
            auto_create_session=True,
        )

    async def call(self, msg: str, state_delta: StateDelta):
        content = types.Content(role="user", parts=[types.Part(text=msg)])

        async for event in self._runner.run_async(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=content,
                state_delta=state_delta.model_dump()
        ):
            response = ''
            for part in event.content.parts:
                if part.function_call:
                    response = AiStreamResponse(
                        type= part.function_call.name,
                        text=f"{part.function_call.name}",
                        finished=False
                    )
                elif part.function_response:
                    response = AiStreamResponse(
                        type= part.function_response.name,
                        text=f"{part.function_response.name}",
                        finished=True
                    )
                elif part.tool_call is not None:
                    response = AiStreamResponse(
                        type= part.tool_call.tool_type.name.lower(),
                        text=f"{part.tool_call.tool_type.name} : {', '.join(part.tool_call.args.get('queries', []))}",
                        finished=False
                    )
                elif part.tool_response:
                    response = AiStreamResponse(
                        type= part.tool_response.tool_type.name,
                        text=f"{part.tool_response.tool_type.name}",
                        finished=True
                    )
                elif part.text:
                    if part.thought:
                        response = AiStreamResponse(
                            type="thinking",
                            text=f"Thinking...",
                            finished=True
                        )
                    else:
                        response = AiStreamResponse(
                            type= "text",
                            text=f"{part.text}",
                            finished=True
                        )
                else:
                    print("---------------------------unknown: ", part)

                yield response.model_dump_json()


    async def get_history(self):
        session = await session_service.get_session(
            app_name="my_app",
            user_id=self.user_id,
            session_id=self.session_id,
        )

        if not session:
            return []

        history = []
        for event in session.events:
            if not event.content or not event.content.parts:
                continue

            for part in event.content.parts:
                if part.text:
                    history.append({
                        "role": event.author,
                        "text": part.text,
                        "timestamp": event.timestamp,
                    })

        return history
