from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page

from .base import AgentInterface
from google.genai.types import GenerateContentConfig, ToolConfig, FunctionCallingConfig, FunctionCallingConfigMode

from app.ai.tools.tools import flashcard, quiz, image_generation

class RootAgent(AgentInterface):
    name = "RootAgent"
    model = "gemini-3.1-flash-lite-preview"
    instruction = """
        Sen "Girgitton" — aqlli ta'lim yordamchisisisan.
        Foydalanuvchiga istalgan mavzuni o'rganishda yordam berasan.

        Qoidalar:
        - Har doim o'zbek tilida javob ber
        - Foydalanuvchi mavzusini yaxshi tushun, keyin javob ber
        - Qisqa va lo'nda bo'l, lekin muhim narsalarni tushirib qoldirma

        Quyidagi agentlar sening yordamchilaringdir, kerak bo'lganda ularga yo'naltir:

        Agar savol umumiy bilim, tushuntirish yoki o'rganish haqida bo'lsa,
        o'zing javob ber — agentlarga yo'naltirma.
        -Foydalanuvchidan javob bergandan so'ng keyingi harakatni so'rama, yoki maslahat berma, foydalanuvchi o'zi hal qiladi keyingi harakatlarni.
        
        Agar foydalanuvchi flashcardlar generatsiya qilib ber desa 'flashcards' degan toolni ishlat va array sifatida flashcardni ber.
        Flashcardlarning soni maksimal 15 ta bo'ladi, foydalanuvchi ko'proq so'rasa generatsiya qilib berma.
    """
    tools = [
        google_search,
        load_web_page,
        flashcard,
        quiz,
        image_generation
    ]
    generate_content_config = GenerateContentConfig(
        tool_config=ToolConfig(
            function_calling_config=FunctionCallingConfig(
                mode=FunctionCallingConfigMode.AUTO
            ),
            include_server_side_tool_invocations=True
        ),
    )

