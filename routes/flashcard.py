from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.core.http import success_response
from app.models import Flashcard
from app.schemes.flashcard_scheme import FlashcardResource, FlashcardItemResource
from app.dependencies.route_dependency import get_valid_flashcard

router = APIRouter()


@router.get("/{flashcard_id}")
async def show(flashcard: Flashcard = Depends(get_valid_flashcard)):
    cards = [FlashcardItemResource.model_validate(card) for card in flashcard.items]
    return success_response(
        data=FlashcardResource(
            id=flashcard.id,
            title=flashcard.title,
            cards=cards
        ), status_code=HTTP_200_OK
    )