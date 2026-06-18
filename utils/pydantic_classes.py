from pydantic import BaseModel

class NewAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: str

class UpdateAgent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank: str | None = None