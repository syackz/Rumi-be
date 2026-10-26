import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket

logger = logging.getLogger("rumi.alerts")

class AlertManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"[WebSocket] Client terhubung. Total aktif: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"[WebSocket] Client terputus. Sisa aktif: {len(self.active_connections)}")

    async def broadcast_fall_alert(self, incident: Dict[str, Any]):
        """Mengirim pesan Fall Alert ke semua client dashboard yang terhubung."""
        message = {
            "type": "FALL_ALERT",
            "title": "Kejadian Jatuh Terdeteksi!",
            "data": incident
        }
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"[WebSocket] Gagal kirim ke client: {e}")
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)

alert_manager = AlertManager()
