from typing import Optional

from pydantic import BaseModel


class VideoCallRequest(BaseModel):
    username: str
    room_id: Optional[str] = None
    identity: Optional[str] = None


class VideoCallResponse(BaseModel):
    token: str
    room_id: str
    identity: str
    username: str


class TokenResult(BaseModel):
    """Result of token creation for LiveKit video calls"""

    identity: str
    token: str
    room_id: str
