from fastapi import APIRouter, HTTPException

from ..models.transcription import TokenResult
from ..services.external.assemblyai import assemblyai_service

router = APIRouter(prefix="/transcription", tags=["transcription"])


@router.post("/token", response_model=TokenResult)
async def create_token():
    """
    Generate a temporary token for AssemblyAI real-time transcription
    This endpoint creates a secure token that your frontend can use
    without exposing the API key.
    """
    try:
        token = assemblyai_service.generate_realtime_token(
            expires_in_seconds=60
        )  # 1 minutes (max allowed)

        return TokenResult(token=token)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate token: {str(e)}"
        )


@router.get("/variables", response_model=dict)
def get_variables():
    """
    Get AssemblyAI configuration variables
    This endpoint returns the API key and other settings used by the service.
    """
    try:
        return assemblyai_service.get_assemblyai_variables()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve variables: {str(e)}"
        )
