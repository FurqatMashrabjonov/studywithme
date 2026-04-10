from google.adk.agents import LlmAgent
from app.ai.tools.tools import flashcard, quiz, image_generation

study_agent = LlmAgent(
    name="StudyAgent",
    model="gemini-2.0-flash",
    instruction="""
        You create study materials.
        Use flashcard, quiz, image_generation tools.
    """,
    tools=[flashcard, quiz, image_generation],
)