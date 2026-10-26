# Folder Model AI - Deteksi Jatuh (Fall Detection)

Folder ini disiapkan khusus untuk integrasi model Computer Vision berbasis YOLOv8 Pose.

### File yang Diharapkan:
1. **`yolov8n-pose.pt`**: File bobot model YOLOv8 Pose hasil training / pre-trained.
2. **`realtime_fall_detection.py`**: Skrip logika deteksi jatuh yang memproses frame video, mengekstrak keypoints tubuh (pose), dan mendeteksi kondisi jatuh (fall).

### Cara Kerja Integrasi:
Backend FastAPI memanggil class `FallDetector` yang ada di dalam `realtime_fall_detection.py`.
Jika file `yolov8n-pose.pt` belum ada, sistem otomatis berjalan dalam **Mode Simulasi (Mock Mode)** sehingga backend tetap bisa dijalankan, dites, dan dihubungkan ke frontend tanpa error.

Setelah rekan Anda selesai membuat model:
1. Letakkan file `yolov8n-pose.pt` di folder ini (`models_ai/yolov8n-pose.pt`).
2. Masukkan atau sesuaikan logika di `realtime_fall_detection.py`.
Backend FastAPI akan langsung menggunakan model asli secara otomatis!
