from typing import Optional

from pydantic import BaseModel


class AssemblyAIRequest(BaseModel):
    expires_in: Optional[int] = 60  # Default to 1 minute, max allowed by AssemblyAI


class AssemblyAIResponse(BaseModel):
    token: str
    expires_in: int
