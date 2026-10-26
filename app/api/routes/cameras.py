from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.camera import CameraCreate, CameraResponse
from app.core.supabase import db

router = APIRouter(prefix="/cameras", tags=["Cameras"])

def detect_protocol(url: str) -> str:
    url_lower = url.lower()
    if url_lower.startswith("rtsp://"):
        return "RTSP"
    return "HTTP"

@router.get("", response_model=List[CameraResponse])
async def list_cameras():
    cameras = await db.get_cameras()
    return [
        CameraResponse(
            id=c["id"],
            name=c["name"],
            location=c["location"],
            url=c.get("url") or c.get("stream_url", ""),
            protocol=c.get("protocol") or detect_protocol(c.get("url") or c.get("stream_url", "")),
            status=c.get("status", "online"),
            created_at=c.get("created_at")
        )
        for c in cameras
    ]

@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def add_camera(camera_in: CameraCreate):
    protocol = detect_protocol(camera_in.url)
    camera_data = {
        "name": camera_in.name,
        "location": camera_in.location,
        "stream_url": camera_in.url,
        "protocol": protocol,
        "status": "online",
        "is_active": True
    }
    created = await db.create_camera(camera_data)
    return CameraResponse(
        id=created["id"],
        name=created["name"],
        location=created["location"],
        url=created.get("stream_url", camera_in.url),
        protocol=created["protocol"],
        status=created["status"],
        created_at=created.get("created_at")
    )

@router.delete("/{camera_id}", status_code=status.HTTP_200_OK)
async def delete_camera(camera_id: str):
    success = await db.delete_camera(camera_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kamera tidak ditemukan")
    return {"message": "Kamera berhasil dihapus", "id": camera_id}
