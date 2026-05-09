"""
Router: /api/collect
สำหรับบันทึก sample ลายมือจาก canvas
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64, os, re
from datetime import datetime

router = APIRouter()

LABELS       = ["๒๑", "๒๒", "๒๓", "๒๔", "๒๕"]
DATASET_DIR  = os.path.join(os.path.dirname(__file__), "..", "..", "dataset")


class SamplePayload(BaseModel):
    label:    str   # เช่น "๒๑"
    image:    str   # base64 PNG จาก canvas.toDataURL()
    writer:   str = "anonymous"  # ชื่อคนเขียน (optional)


def _next_index(label_dir: str) -> int:
    """นับไฟล์ที่มีอยู่แล้ว แล้วบวก 1"""
    existing = [f for f in os.listdir(label_dir) if f.endswith(".png")]
    return len(existing) + 1


@router.post("/save-sample")
async def save_sample(payload: SamplePayload):
    """รับภาพ base64 จาก frontend แล้วบันทึกเป็น PNG"""
    if payload.label not in LABELS:
        raise HTTPException(400, f"label ต้องเป็นหนึ่งใน {LABELS}")

    # แปลง base64 → bytes
    try:
        img_data = re.sub(r"^data:image/png;base64,", "", payload.image)
        img_bytes = base64.b64decode(img_data)
    except Exception:
        raise HTTPException(400, "รูปแบบ image ไม่ถูกต้อง ต้องเป็น base64 PNG")

    label_dir = os.path.join(DATASET_DIR, payload.label)
    os.makedirs(label_dir, exist_ok=True)

    idx      = _next_index(label_dir)
    # ชื่อไฟล์: เช่น 21_042_20250501_153012.png
    thai_to_arabic = {"๒๑":"21","๒๒":"22","๒๓":"23","๒๔":"24","๒๕":"25"}
    arabic   = thai_to_arabic[payload.label]
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{arabic}_{idx:03d}_{ts}.png"
    filepath = os.path.join(label_dir, filename)

    with open(filepath, "wb") as f:
        f.write(img_bytes)

    return {
        "success":  True,
        "filename": filename,
        "label":    payload.label,
        "index":    idx,
        "message":  f"บันทึกสำเร็จ: {filename}",
    }


@router.delete("/delete-last/{label}")
async def delete_last(label: str):
    """ลบไฟล์ล่าสุดของ label นั้น (กรณีเขียนผิด)"""
    if label not in LABELS:
        raise HTTPException(400, "label ไม่ถูกต้อง")

    label_dir = os.path.join(DATASET_DIR, label)
    files = sorted([f for f in os.listdir(label_dir) if f.endswith(".png")])
    if not files:
        raise HTTPException(404, "ไม่มีไฟล์ให้ลบ")

    last = os.path.join(label_dir, files[-1])
    os.remove(last)
    return {"success": True, "deleted": files[-1]}
