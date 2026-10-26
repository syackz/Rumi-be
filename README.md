# Rumi Backend API (FastAPI + Supabase)

Backend REST API & WebSocket Real-time Alert untuk sistem **Rumi: Deteksi Jatuh & Monitoring CCTV**.

---

## 🚀 Fitur Utama

- **Autentikasi & Akun**: Register, Login, JWT Token Bearer, Profil Pengguna.
- **Kamera CCTV**: CRUD stream kamera (HTTP / MJPEG dan RTSP).
- **Riwayat Insiden**: Pencatatan deteksi jatuh, bukti snapshot foto, dan filter riwayat (hari & lokasi).
- **Dashboard Summary**: Metrik KPI (kamera aktif, latensi alert, uptime, grafik mingguan).
- **Model Deteksi Jatuh Adapter**:
  - Slot siap pakai untuk `yolov8n-pose.pt` dan `realtime_fall_detection.py`.
  - Dilengkapi mode simulasi / fallback jika model sedang dalam proses pembuatan oleh tim lain.
  - Endpoint trigger simulasi insiden untuk pengujian.
- **Real-time Alerting (WebSocket)**: Mengirim sinyal alarm instan ke dashboard begitu model mendeteksi insiden jatuh.
- **Integrasi Database Supabase**: Skrip SQL DDL siap pakai di folder `supabase/schema.sql`.

---

## 🛠️ Panduan Instalasi & Menjalankan

### 1. Buat Virtual Environment & Install Dependensi
Buka terminal di folder `Rumi-be`:

```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Atau CMD:
.\venv\Scripts\activate.bat

# Install dependensi
pip install -r requirements.txt
```

### 2. Konfigurasi Environment (`.env`)
Salin file `.env.example` menjadi `.env` (sudah disediakan defaultnya):
```env
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-or-service-role-key"
```
> *Catatan:* Jika kredensial Supabase belum diisi, sistem otomatis berjalan dengan in-memory database demo sehingga tetap bisa ditest dan didevelop!

### 3. Setup Database Supabase
1. Buka dashboard proyek Anda di [Supabase](https://supabase.com).
2. Masuk ke menu **SQL Editor** -> **New Query**.
3. Buka file [supabase/schema.sql](file:///c:/Users/USER/Documents/Viskom_Citra/Rumi-be/supabase/schema.sql), salin seluruh isinya dan klik **Run**.
4. Semua tabel (`users`, `cameras`, `incidents`, `user_settings`) dan data awal demo akan otomatis terbuat.

### 4. Menjalankan Server Backend
```powershell
python run.py
```
Atau menggunakan uvicorn langsung:
```powershell
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🤖 Integrasi Model AI (`yolov8n-pose.pt`)

Ketika rekan Anda telah menyelesaikan model deteksi jatuh:
1. Simpan file bobot model di: `models_ai/yolov8n-pose.pt`.
2. Sesuaikan atau masukkan logika pemrosesan di: `models_ai/realtime_fall_detection.py`.
3. Pasang library ultralytics: `pip install ultralytics`.

Endpoint backend di `app/api/routes/model.py` dan WebSocket alert akan otomatis beralih menggunakan model asli tanpa perlu mengubah rute API!
