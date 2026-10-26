from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
from models_ai.realtime_fall_detection import detector
from app.core.supabase import db
from app.services.alert_manager import alert_manager
import uuid

router = APIRouter(prefix="/model", tags=["AI Model & Vision"])

@router.get("/status")
async def get_model_status():
    """Cek status kesiapan file model yolov8n-pose.pt."""
    return {
        "model_file": detector.model_path,
        "is_model_loaded": detector.is_loaded,
        "mode": "YOLOv8-Pose (Active)" if detector.is_loaded else "Mock / Adapter Mode (Waiting for yolov8n-pose.pt)",
        "message": (
            "Model YOLOv8 Pose aktif!"
            if detector.is_loaded
            else f"Letakkan file 'yolov8n-pose.pt' di folder 'models_ai/' dan install ultralytics untuk mengaktifkan model asli."
        )
    }

@router.post("/detect-frame")
async def detect_frame(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Menerima 1 frame gambar untuk dianalisis oleh detector."""
    try:
        content = await file.read()
        result = detector.process_frame(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses frame: {str(e)}")

@router.post("/simulate-fall")
async def trigger_simulated_fall():
    """
    Endpoint pengujian: Menstimulasi kejadian jatuh buatan.
    Ini akan membuat record baru di database dan mengirim Fall Alert secara real-time ke WebSocket.
    """
    result = detector.simulate_fall()

    incident_data = {
        "id": str(uuid.uuid4()),
        "camera_name": "Ruang Tamu · Cam 01",
        "location": "Ruang Tamu",
        "person_name": "Pak Hartono",
        "confidence": result["confidence"],
        "snapshot_url": "/static/uploads/fall-snapshot.jpg",
        "clip_duration": "8 dtk",
        "response_time_seconds": 2.1,
        "status": "unresolved"
    }

    saved = await db.create_incident(incident_data)
    await alert_manager.broadcast_fall_alert(saved)

    return {
        "message": "Simulasi kejadian jatuh berhasil dipicu dan di-broadcast!",
        "detection": result,
        "incident": saved
    }
