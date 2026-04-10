from fastapi import APIRouter
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.responses import StreamingResponse
from app.core.http import success_response
from app.dependencies.route_dependency import get_valid_notebook
from app.dependencies.security_dependency import get_request_user
from app.models import User, Notebook
from app.ai.orchestrator import Orchestrator
from app.schemes.ai_scheme import AiRequest, StateDelta

load_dotenv()
router = APIRouter()

@router.post("/chat")
async def chat(
        request: AiRequest,
        user: User = Depends(get_request_user),
        notebook: Notebook = Depends(get_valid_notebook)
):
    orchestrator = Orchestrator(user_id=str(user.id), session_id=str(notebook.uid))
    state_delta = StateDelta(
        notebook_id=notebook.id
    )

    return StreamingResponse(
        orchestrator.call(request.message, state_delta=state_delta),
        media_type="text/event-stream"
    )
@router.get("/history")
async def get_history(
    user: User = Depends(get_request_user),
    notebook: Notebook = Depends(get_valid_notebook)
):
    orchestrator = Orchestrator(
        user_id=str(user.id),
        session_id=str(notebook.uid)
    )
    history = await orchestrator.get_history()
    return {"history": history}