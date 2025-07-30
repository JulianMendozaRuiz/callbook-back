from fastapi import APIRouter, HTTPException

from app.models.videocall import VideoCallRequest, VideoCallResponse
from app.services.external.livekit import (
    create_video_call,
    get_all_rooms,
    get_livekit_variables,
    get_room_info,
    join_video_call,
)

router = APIRouter(prefix="/videocall", tags=["videocall"])


@router.post("/create-call", response_model=VideoCallResponse)
async def create_call(request: VideoCallRequest):
    """
    Create a new video call room and token for LiveKit

    - **username**: Display name for the user
    - **identity**: Optional user identity (auto-generated if not provided)
    """

    # Create room and get token result from the service
    result = await create_video_call(
        username=request.username, identity=request.identity
    )

    return VideoCallResponse(
        token=result.token,
        room_id=result.room_id,
        identity=result.identity,
        username=request.username,
    )


@router.post("/join-call", response_model=VideoCallResponse)
def join_call(request: VideoCallRequest):
    """
    Join an existing video call room

    - **username**: Display name for the user
    - **room_id**: ID of the room to join
    - **identity**: Optional user identity (auto-generated if not provided)
    """
    if not request.room_id:
        raise HTTPException(
            status_code=400, detail="room_id is required to join a call"
        )

    # Check if room exists
    room_info = get_room_info(request.room_id)
    if not room_info:
        raise HTTPException(status_code=404, detail=f"Room {request.room_id} not found")

    result = join_video_call(
        username=request.username, room_id=request.room_id, identity=request.identity
    )

    return VideoCallResponse(
        token=result.token,
        room_id=result.room_id,
        identity=result.identity,
        username=request.username,
    )


@router.get("/rooms")
def list_rooms():
    """
    Get all active rooms
    """
    return get_all_rooms()


@router.get("/rooms/{room_id}")
def get_room(room_id: str):
    """
    Get information about a specific room
    """
    room_info = get_room_info(room_id)
    if not room_info:
        raise HTTPException(status_code=404, detail="Room not found")
    return room_info


@router.get("/variables")
def get_variables():
    """
    Get environment variables related to video calls
    """
    return get_livekit_variables()
