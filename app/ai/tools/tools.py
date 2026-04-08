from pydantic import TypeAdapter
from typing import List
from app.ai.scheme import FlashcardWrapper, Flashcard, QuizWrapper, QuizQuestion, ImageGenerationPrompt
from google.adk.tools import ToolContext
from google import genai
import os
from datetime import datetime
from app.core.config import settings

def flashcard(card_wrapper: FlashcardWrapper, tool_context: ToolContext):
    adapter = TypeAdapter(List[Flashcard])
    validated_cards = adapter.validate_python(card_wrapper.cards)

    print(f"Nomi: {card_wrapper.title}")

    for card in validated_cards:
        print(f"Savol: {card.question}: {card.answer}")

    print("Notebook uid: ", tool_context.state.get('notebook_id'))

    return {"status": "success", "count": len(validated_cards)}


def quiz(quiz_wrapper: QuizWrapper, tool_context: ToolContext):
    adapter = TypeAdapter(List[QuizQuestion])
    validated_questions = adapter.validate_python(quiz_wrapper.questions)

    print(f"Nomi: {quiz_wrapper.title}")

    for question in validated_questions:
        print(f"Savol: {question.question}:")
        for option in question.options:
            t = question.options[option]
            if option == question.correct_option:
                option = f"({option})"
            print(f"{option}  {t}")

    return {"status": "success"}

def image_generation(prompt: ImageGenerationPrompt, tool_context: ToolContext):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt.prompt],
    )

    os.makedirs("storage/images", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"storage/images/generated_image_{timestamp}.png"

    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(path)

    return {"status": "success", "path": path}