from pydantic import BaseModel


class VoxRequest(BaseModel):
    text: str
