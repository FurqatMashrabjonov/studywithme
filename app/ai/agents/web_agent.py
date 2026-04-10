from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page

web_agent = LlmAgent(
    name="WebAgent",
    model="gemini-2.0-flash",
    instruction="""
        You are a web researcher.
        Use google_search to search, load_web_page to read URLs.
        Always return what you found.
    """,
    tools=[google_search, load_web_page],
)