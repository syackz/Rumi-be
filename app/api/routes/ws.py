from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.alert_manager import alert_manager
import logging

logger = logging.getLogger("rumi.ws")

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            # Tetap jaga koneksi tetap hidup dengan mendengarkan ping/pong
            data = await websocket.receive_text()
            # Echo heartbeat
            await websocket.send_text('{"type": "PONG"}')
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"[WebSocket] Exception: {e}")
        alert_manager.disconnect(websocket)
