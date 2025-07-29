from fastapi import APIRouter

from app.models.videocall import VideoCallRequest, VideoCallResponse
from app.services.external.livekit import create_video_call

router = APIRouter(prefix="/videocall", tags=["videocall"])


@router.post("/create-call", response_model=VideoCallResponse)
def create_call(request: VideoCallRequest):
    """
    Create a new video call token for LiveKit

    - **username**: Display name for the user
    - **identity**: Optional user identity (auto-generated if not provided)
    """

    # Get token result from the service
    result = create_video_call(username=request.username, identity=request.identity)

    return VideoCallResponse(
        token=result.token,
        room_id=result.room_id,
        identity=result.identity,
        username=request.username,
    )


@router.post("/join-call", response_model=VideoCallResponse)
def join_call(request: VideoCallRequest):
    return VideoCallResponse(
        token="",
        room_id=request.room_id or "",
        identity="",
        username="",
    )
