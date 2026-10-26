from fastapi import APIRouter, Query, status
from typing import List, Optional
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.core.supabase import db
from app.services.alert_manager import alert_manager

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponse])
async def list_incidents(
    days: Optional[int] = Query(None, description="Filter hari terakhir, cth: 7, 30, 90"),
    location: Optional[str] = Query(None, description="Filter lokasi kamera, cth: ruang-tamu, all")
):
    incidents = await db.get_incidents(days=days, location=location)
    return [
        IncidentResponse(
            id=inc["id"],
            camera_id=inc.get("camera_id"),
            camera_name=inc.get("camera_name", "Kamera CCTV"),
            location=inc.get("location", "Ruang Tamu"),
            person_name=inc.get("person_name", "Pak Hartono"),
            detected_at=inc.get("detected_at", ""),
            confidence=float(inc.get("confidence", 0.95)),
            snapshot_url=inc.get("snapshot_url") or "/static/uploads/fall-snapshot.jpg",
            clip_duration=inc.get("clip_duration", "8 dtk"),
            response_time_seconds=float(inc.get("response_time_seconds", 2.4)),
            status=inc.get("status", "unresolved")
        )
        for inc in incidents
    ]

@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(incident_in: IncidentCreate):
    incident_data = incident_in.model_dump()
    created = await db.create_incident(incident_data)

    # Broadcast ke WebSocket client secara real-time
    await alert_manager.broadcast_fall_alert(created)

    return IncidentResponse(
        id=created["id"],
        camera_id=created.get("camera_id"),
        camera_name=created["camera_name"],
        location=created["location"],
        person_name=created["person_name"],
        detected_at=created["detected_at"],
        confidence=float(created["confidence"]),
        snapshot_url=created.get("snapshot_url"),
        clip_duration=created.get("clip_duration", "8 dtk"),
        response_time_seconds=float(created.get("response_time_seconds", 2.4)),
        status=created["status"]
    )
