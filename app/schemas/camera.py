from pydantic import BaseModel, Field
from typing import Optional, Literal

class CameraCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., description="Stream URL (HTTP, HTTPS, or RTSP)")

class CameraResponse(BaseModel):
    id: str
    name: str
    location: str
    url: str
    protocol: Literal["HTTP", "RTSP"]
    status: Literal["online", "offline"] = "online"
    created_at: Optional[str] = None
