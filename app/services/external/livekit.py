import os
import random
import string
import uuid
from datetime import datetime
from typing import Dict, Optional

from dotenv import load_dotenv
from livekit import api

from app.models.videocall import TokenResult

# Load environment variables from .env file
load_dotenv()

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "secret")


class LiveKitService:
    """Singleton service for LiveKit API operations"""

    _instance: Optional["LiveKitService"] = None
    _api_client: Optional[api.LiveKitAPI] = None
    _rooms: Dict[str, dict] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _initialize(self):
        """Initialize the LiveKit API client"""
        if self._api_client is None:
            self._api_client = api.LiveKitAPI(
                url=LIVEKIT_URL,
                api_key=LIVEKIT_API_KEY,
                api_secret=LIVEKIT_API_SECRET,
            )
        if not hasattr(self, "_rooms") or self._rooms is None:
            self._rooms = {}

    @property
    def api_client(self) -> api.LiveKitAPI:
        """
        Get the LiveKit API client instance.

        This property lazily initializes the API client if it has not been created yet.
        Raises an exception if the API client could not be initialized.
        """
        if self._api_client is None:
            self._initialize()
        if self._api_client is None:
            raise RuntimeError("LiveKitAPI client could not be initialized.")
        return self._api_client

    def store_room(self, room_id: str, creator_identity: str, creator_username: str):
        """Store room information in memory"""
        self._rooms[room_id] = {
            "room_id": room_id,
            "creator_identity": creator_identity,
            "creator_username": creator_username,
            "created_at": datetime.now().isoformat(),
            "participants": [creator_identity],
        }

    def get_room(self, room_id: str) -> Optional[dict]:
        """Get room information from memory"""
        return self._rooms.get(room_id)

    def add_participant(self, room_id: str, participant_identity: str):
        """Add a participant to a room"""
        if room_id in self._rooms:
            if participant_identity not in self._rooms[room_id]["participants"]:
                self._rooms[room_id]["participants"].append(participant_identity)

    def get_all_rooms(self) -> Dict[str, dict]:
        """Get all stored rooms"""
        return self._rooms

    def remove_room(self, room_id: str):
        """Remove room from memory"""
        if room_id in self._rooms:
            del self._rooms[room_id]


# Global singleton instance
livekit_service = LiveKitService()


def generate_room_id(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_token(
    name: str, identity: str | None = None, room_name: str | None = None
) -> TokenResult:
    identity = identity or str(uuid.uuid4())  # unique user identity
    room_name = room_name or f"{name}-{generate_room_id()}"

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(name)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
            )
        )
    )
    return TokenResult(identity=identity, token=token.to_jwt(), room_id=room_name)


async def create_video_call(
    username: str,
    identity: str | None = None,
) -> TokenResult:
    """
    Create a new video call room and return a token for the creator
    """
    identity = identity or str(uuid.uuid4())
    sanitized_username = username.replace(" ", "_")
    room_name = f"{sanitized_username}-{generate_room_id()}"

    # Use singleton LiveKit API client
    await livekit_service.api_client.room.create_room(
        api.CreateRoomRequest(
            name=room_name,
            empty_timeout=5 * 60,  # 5 minutes
            max_participants=2,  # Default max participants
        )
    )

    # Store room information in memory
    livekit_service.store_room(
        room_id=room_name, creator_identity=identity, creator_username=username
    )

    # Generate token for the room creator
    return create_token(name=username, identity=identity, room_name=room_name)


def join_video_call(
    username: str,
    room_id: str,
    identity: str | None = None,
) -> TokenResult:
    """
    Generate a token to join an existing video call room
    """
    identity = identity or str(uuid.uuid4())

    # Add participant to room if it exists
    livekit_service.add_participant(room_id, identity)

    return create_token(name=username, identity=identity, room_name=room_id)


def get_room_info(room_id: str) -> Optional[dict]:
    """Get room information"""
    return livekit_service.get_room(room_id)


def get_all_rooms() -> Dict[str, dict]:
    """Get all rooms"""
    return livekit_service.get_all_rooms()


def get_livekit_variables():
    return {
        "LIVEKIT_URL": LIVEKIT_URL,
        "LIVEKIT_API_KEY": LIVEKIT_API_KEY,
        "LIVEKIT_API_SECRET": LIVEKIT_API_SECRET,
    }
