from pydantic import BaseModel


class VoxRequest(BaseModel):
    model: str | None = None
    style: int | None = None
    text: str
