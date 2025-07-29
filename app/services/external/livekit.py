import os
import random
import string
import uuid

from livekit import api

from app.models.videocall import TokenResult

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "secret")


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


def create_video_call(
    username: str,
    identity: str | None = None,
) -> TokenResult:
    return create_token(name=username, identity=identity)
