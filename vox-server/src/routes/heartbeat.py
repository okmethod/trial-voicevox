from fastapi import APIRouter

from src.schemas.heartbeat import HeartbeatResponse

router = APIRouter()


@router.get(
    path="",
)
def heartbeat() -> HeartbeatResponse:
    return HeartbeatResponse(message="alive")
