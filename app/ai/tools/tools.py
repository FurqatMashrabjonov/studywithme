from google.adk.tools import ToolContext
from google import genai
from pydantic import TypeAdapter
from typing import List
from app.ai.scheme import FlashcardWrapper, Flashcard, QuizWrapper, QuizQuestion, ImageGenerationPrompt
from app.core.config import settings
import os
from datetime import datetime
from google.genai import types

def flashcard(title: str, cards: list[dict], tool_context: ToolContext) -> dict:
    """
    Creates flashcards for studying.

    Args:
        title: Title or topic of the flashcard set.
        cards: List of flashcards, each with 'question' and 'answer' keys.
        tool_context: ADK tool context (injected automatically).

    Returns:
        Status and count of created flashcards.
    """
    adapter = TypeAdapter(List[Flashcard])
    validated_cards = adapter.validate_python(cards)

    print(f"Nomi: {title}")
    for card in validated_cards:
        print(f"Savol: {card.question}: {card.answer}")

    print("Notebook uid: ", tool_context.state.get('notebook_id'))

    return {"status": "success", "count": len(validated_cards)}


def quiz(title: str, questions: list[dict], tool_context: ToolContext) -> dict:
    """
    Creates a quiz with multiple choice questions.

    Args:
        title: Title of the quiz.
        questions: List of questions, each with 'question', 'options' (dict), and 'correct_option' keys.
        tool_context: ADK tool context (injected automatically).

    Returns:
        Status of quiz creation.
    """
    adapter = TypeAdapter(List[QuizQuestion])
    validated_questions = adapter.validate_python(questions)

    print(f"Nomi: {title}")
    for question in validated_questions:
        print(f"Savol: {question.question}:")
        for option, text in question.options.items():
            label = f"({option})" if option == question.correct_option else option
            print(f"{label}  {text}")

    return {"status": "success"}


def image_generation(prompt: str, tool_context: ToolContext) -> dict:
    """
    Generates an image based on a text prompt.

    Args:
        prompt: Detailed text description of the image to generate.
        tool_context: ADK tool context (injected automatically).

    Returns:
        Status and file path of the generated image.
    """
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
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

def artifact_finder(subject: str) -> dict:
    """
    Finds websites, youtube videos or articles according to subject.

    Args:
        subject: Subject of finding artifacts.
        tool_context: ADK tool context (injected automatically).

    Returns:
        Status and list of artifacts.
    """
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[
            f"""
            You are a learning resource curator. Search the internet for the TOP 10 best resources to study this topic: {subject}

            Return ONLY a valid JSON object. No markdown, no explanation, no extra text.

            Format:
            {{
                "resources": [
                    {{
                        "title": "Resource title",
                        "url": "https://...",
                        "type": "video | website | article | book | podcast",
                        "difficulty": "Beginner | Intermediate | Advanced",
                        "description": "Why it's recommended (2-3 sentences)",
                        "estimated_time": "e.g. 2 hours"
                    }}
                ]
            }}

            Include a mix of YouTube videos, websites/courses, articles, and books.
            Focus on free resources first. Sort from Beginner to Advanced.
            """
        ],
        config=config
    )

    import json
    import re

    raw = response.text.strip()

    raw = re.sub(r"```(?:json)?", "", raw).strip()

    parsed = json.loads(raw)
    resources = parsed.get("resources", [])

    print(resources)

    return {
        "status": "success",
        "subject": subject,
        "resources": resources,
        "urls": [r["url"] for r in resources]
    }