from pydantic import BaseModel

class AgentResponse(BaseModel):
    text: str
    token: object
