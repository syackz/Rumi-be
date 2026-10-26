"""
realtime_fall_detection.py
Modul Deteksi Jatuh Real-time menggunakan YOLOv8 Pose.
File ini dirancang agar siap menerima model asli `yolov8n-pose.pt`.
Jika model belum tersedia, sistem akan otomatis berjalan dalam mode fallback/simulasi.
"""

import os
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("rumi.model")

class FallDetector:
    def __init__(self, model_path: str = "models_ai/yolov8n-pose.pt"):
        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        """Memuat model YOLOv8 Pose jika file dan library ultralytics tersedia."""
        if not os.path.exists(self.model_path):
            logger.warning(
                f"[FallDetector] File model '{self.model_path}' belum ditemukan. "
                "Berjalan dalam mode Simulasi/Adapter sampai file diletakkan."
            )
            return

        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            self.is_loaded = True
            logger.info(f"[FallDetector] Berhasil memuat YOLO model dari {self.model_path}")
        except ImportError:
            logger.warning(
                "[FallDetector] Library 'ultralytics' belum terinstall. "
                "Jalankan 'pip install ultralytics' saat model siap."
            )
        except Exception as e:
            logger.error(f"[FallDetector] Gagal memuat model: {e}")

    def process_frame(self, frame_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Memproses satu frame gambar untuk mendeteksi pose dan kemungkinan jatuh.
        
        Args:
            frame_data: data binary gambar (JPEG/PNG)
            
        Returns:
            Dict berisi status deteksi, confidence, dan koordinat.
        """
        start_time = time.time()

        # JIKA MODEL ASLI SUDAH DIMUAT
        if self.is_loaded and self.model is not None and frame_data is not None:
            try:
                import io
                from PIL import Image
                image = Image.open(io.BytesIO(frame_data)).convert("RGB")
                
                # Jalankan inferensi YOLOv8-pose
                results = self.model(image, verbose=False)
                latency = round((time.time() - start_time) * 1000, 2)
                
                for r in results:
                    if r.keypoints is not None and len(r.keypoints) > 0:
                        # Logika deteksi jatuh berbasis keypoints pose (YOLOv8-pose)
                        # Misalnya: perbandingan tinggi bounding box vs lebar, atau posisi kepala vs pinggul
                        boxes = r.boxes.xyxy.cpu().numpy()
                        if len(boxes) > 0:
                            x1, y1, x2, y2 = boxes[0]
                            width = x2 - x1
                            height = y2 - y1
                            
                            # Ciri umum jatuh: aspek rasio melebar (lebar > tinggi)
                            is_fallen = width > (height * 1.1)
                            conf = float(r.boxes.conf[0]) if len(r.boxes.conf) > 0 else 0.85
                            
                            return {
                                "fall_detected": bool(is_fallen),
                                "confidence": round(conf, 2),
                                "person_detected": True,
                                "status": "FALL_DETECTED" if is_fallen else "NORMAL",
                                "bounding_box": [float(x1), float(y1), float(x2), float(y2)],
                                "latency_ms": latency,
                                "source": "yolov8n-pose"
                            }

                return {
                    "fall_detected": False,
                    "confidence": 0.0,
                    "person_detected": False,
                    "status": "NO_PERSON",
                    "bounding_box": None,
                    "latency_ms": latency,
                    "source": "yolov8n-pose"
                }
            except Exception as e:
                logger.error(f"[FallDetector] Error saat inferensi model: {e}")

        # MODE SIMULASI / PLACEHOLDER (JIKA FILE MODEL BELUM ADA)
        latency = round((time.time() - start_time) * 1000, 2)
        return {
            "fall_detected": False,
            "confidence": 0.94,
            "person_detected": True,
            "status": "NORMAL",
            "bounding_box": [120.0, 80.0, 340.0, 480.0],
            "latency_ms": latency if latency > 0 else 24.5,
            "source": "mock_adapter"
        }

    def simulate_fall(self) -> Dict[str, Any]:
        """Method helper untuk menguji trigger insiden jatuh langsung dari backend."""
        return {
            "fall_detected": True,
            "confidence": 0.97,
            "person_detected": True,
            "status": "FALL_DETECTED",
            "bounding_box": [80.0, 250.0, 460.0, 390.0],
            "latency_ms": 32.1,
            "source": "simulation_trigger"
        }

# Instance global singleton
detector = FallDetector()
