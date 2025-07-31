from pydantic import BaseModel


class TokenResult(BaseModel):
    token: str
