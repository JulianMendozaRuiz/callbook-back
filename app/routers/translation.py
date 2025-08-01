from fastapi import APIRouter, HTTPException

from ..models.translation import (
    TranslateRequest,
    TranslateResponse,
)
from ..services.external.google_translate import google_translate_service

router = APIRouter(prefix="/translation", tags=["translation"])


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text to target language

    - **text**: Text to translate
    - **target_language**: Target language code (e.g., 'es', 'fr', 'de')
    - **source_language**: Source language code (optional, auto-detected if not provided)
    """
    try:
        result = google_translate_service.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=request.source_language,
        )

        return TranslateResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
