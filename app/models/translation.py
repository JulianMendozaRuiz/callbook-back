from typing import Optional

from pydantic import BaseModel


class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class TranslateResponse(BaseModel):
    translatedText: str
    detectedSourceLanguage: Optional[str]
    input: str
    targetLanguage: str
