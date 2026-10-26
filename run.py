import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 Menjalankan Server Backend Rumi (FastAPI)...")
    print("  📖 Dokumentasi API Swagger: http://localhost:8000/docs")
    print("  📡 WebSocket Alert Endpoint: ws://localhost:8000/ws/alerts")
    print("=" * 60)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
