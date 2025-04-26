from pydantic import BaseModel


class HeartbeatResponse(BaseModel):
    message: str
