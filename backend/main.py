"""
Thai Digit Collector — Backend (FastAPI)
ระบบเก็บ dataset ลายมือเขียนเลขไทย ๒๑–๒๕
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from routers import collect, predict, admin, stats

# ─── สร้างโฟลเดอร์ dataset ถ้ายังไม่มี ───────────────────────────────────────
LABELS = ["๒๑", "๒๒", "๒๓", "๒๔", "๒๕"]
DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")

@asynccontextmanager
async def lifespan(app: FastAPI):
    for label in LABELS:
        os.makedirs(os.path.join(DATASET_DIR, label), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "models"), exist_ok=True)
    yield

# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Thai Digit Collector API",
    description="API สำหรับเก็บ dataset และ predict เลขไทย ๒๑–๒๕",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(collect.router,  prefix="/api/collect",  tags=["Dataset Collection"])
app.include_router(predict.router,  prefix="/api/predict",  tags=["Prediction"])
app.include_router(admin.router,    prefix="/api/admin",    tags=["Admin"])
app.include_router(stats.router,    prefix="/api/stats",    tags=["Statistics"])

# ─── Serve Frontend ───────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def serve_user_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "user.html"))

@app.get("/admin")
async def serve_admin_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

@app.get("/collect")
async def serve_collect_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "collect.html"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
