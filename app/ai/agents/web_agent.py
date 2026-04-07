from google.adk.tools import google_search

from .base import AgentInterface
from google.genai.types import GenerateContentConfig, ToolConfig, FunctionCallingConfig, FunctionCallingConfigMode


class WebAgent(AgentInterface):
    name = "WebAgent"
    model = "gemini-3.1-flash-lite-preview"
    instruction = """
        Sen internetdan ma'lumot qidirib beruvchi yordamchi agentsan.

        Vazifang:
        - Foydalanuvchi so'ragan mavzu bo'yicha google_search orqali eng yangi va ishonchli ma'lumotlarni top
        - Bir nechta qidiruv so'rovlari orqali to'liq va aniq ma'lumot yig'
        - Topilgan ma'lumotlarni o'zbek tilida tushunarli va tizimli tarzda taqdim et
        - Manbalarni ko'rsat va ma'lumotning qanchalik yangiligini bildir
        - Agar ma'lumot topilmasa, foydalanuvchiga aniq ayt va boshqa usulda qidirishni taklif qil
    """
    tools = [google_search]
    generate_content_config = GenerateContentConfig(
        tool_config=ToolConfig(
            function_calling_config=FunctionCallingConfig(
                mode=FunctionCallingConfigMode.AUTO
            ),
            include_server_side_tool_invocations=True
        ),
    )