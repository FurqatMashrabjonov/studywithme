from typing import List, Any

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig


class AgentInterface:
    name: str
    model: str
    instruction: str
    tools: List = []
    sub_agents: List = []
    generate_content_config: GenerateContentConfig | None
    _agent: Agent = None

    def __init__(self):
        self._agent = Agent(
            name=self.name,
            model=self.model,
            instruction=self.instruction,
            generate_content_config=self.generate_content_config,
            sub_agents=self.sub_agents
        )

    def get_agent(self):
        return self._agent




