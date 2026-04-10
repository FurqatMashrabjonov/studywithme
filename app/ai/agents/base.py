from typing import List
from google.adk.planners import BuiltInPlanner
from google.genai import types
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
            tools=self.tools,
            generate_content_config=self.generate_content_config,
            sub_agents=self.sub_agents,
            planner=BuiltInPlanner(
                thinking_config=types.ThinkingConfig(
                    include_thoughts=True,  # Surfaces thoughts in events
                    thinking_budget=2048,  # Sets maximum reasoning tokens
                )
            )
        )

    def get_agent(self):
        return self._agent




