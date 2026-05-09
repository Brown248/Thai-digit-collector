"""
Router: /api/admin
สำหรับ Admin อัปโหลด model ใหม่เข้าระบบ (hot-reload โดยไม่ restart server)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
import os, shutil
from datetime import datetime

router     = APIRouter()
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
ALLOWED    = {".pkl", ".joblib", ".h5", ".pt"}


@router.post("/upload-model")
async def upload_model(file: UploadFile = File(...)):
    """อัปโหลด model ไฟล์ใหม่ แล้ว hot-reload ทันที"""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(400, f"ไฟล์ต้องเป็น {ALLOWED}")

    os.makedirs(MODELS_DIR, exist_ok=True)

    # ตั้งชื่อไฟล์ใหม่พร้อม timestamp เพื่อไม่ให้ทับของเดิม
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"model_{ts}{ext}"
    dest     = os.path.join(MODELS_DIR, filename)

    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Hot-reload: reset singleton ใน predict router
    import routers.predict as pred_router
    try:
        # ต้อง unpack tuple (model, type) ออกมา
        pred_router._model, pred_router._model_type = pred_router.load_model_file(dest)
        pred_router._model_name = filename
        loaded = True
        msg    = f"โหลด model '{filename}' สำเร็จ"
    except Exception as e:
        loaded = False
        msg    = f"บันทึกไฟล์สำเร็จ แต่โหลด model ไม่ได้: {str(e)}"

    return {
        "success":  True,
        "filename": filename,
        "loaded":   loaded,
        "message":  msg,
    }


@router.get("/models")
async def list_models():
    """แสดงรายการ model ทั้งหมดใน /models"""
    if not os.path.exists(MODELS_DIR):
        return {"models": []}
    files = sorted([
        f for f in os.listdir(MODELS_DIR)
        if os.path.splitext(f)[1].lower() in ALLOWED
    ], reverse=True)
    return {"models": files}


@router.delete("/models/{filename}")
async def delete_model(filename: str):
    """ลบ model ไฟล์ที่ระบุ"""
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "ไม่พบไฟล์")
    os.remove(path)
    return {"success": True, "deleted": filename}
