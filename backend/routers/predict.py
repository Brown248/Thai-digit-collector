"""
Router: /api/predict
รับภาพจาก canvas แล้ว predict ด้วย model ที่โหลดไว้
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64, re, io, os
import numpy as np

router = APIRouter()

# ─── Model State (shared singleton) ──────────────────────────────────────────
_model       = None
_model_name  = "ยังไม่ได้โหลด model"
MODELS_DIR   = os.path.join(os.path.dirname(__file__), "..", "..", "models")
LABELS       = ["๒๑", "๒๒", "๒๓", "๒๔", "๒๕"]
IMG_SIZE     = 32  # resize เป็น 32x32 ให้ตรงกับ model ที่ train ใหม่


def load_model_file(path: str):
    """โหลด model จากไฟล์ .pkl / .joblib / .h5 / .pt"""
    import joblib
    ext = os.path.splitext(path)[1].lower()
    if ext in (".pkl", ".joblib"):
        return joblib.load(path)
    elif ext == ".h5":
        from tensorflow.keras.models import load_model as keras_load
        return keras_load(path)
    elif ext == ".pt":
        import torch
        try:
            model = torch.jit.load(path, map_location="cpu")
        except:
            model = torch.load(path, map_location="cpu", weights_only=False)
        model.eval()
        return model
    raise ValueError(f"ไม่รองรับ format: {ext}")


def get_model():
    global _model, _model_name
    if _model is None:
        # ลองโหลด model ล่าสุดจาก models/
        files = sorted([
            f for f in os.listdir(MODELS_DIR)
            if f.endswith((".pkl", ".joblib", ".h5", ".pt"))
        ]) if os.path.exists(MODELS_DIR) else []
        if files:
            path = os.path.join(MODELS_DIR, files[-1])
            _model = load_model_file(path)
            _model_name = files[-1]
    return _model


def preprocess_image(b64_str: str) -> np.ndarray:
    """แปลง base64 PNG → numpy array ขนาด (1, 28*28) หรือ (1, 28, 28, 1)"""
    from PIL import Image
    img_data  = re.sub(r"^data:image/png;base64,", "", b64_str)
    img_bytes = base64.b64decode(img_data)
    img       = Image.open(io.BytesIO(img_bytes)).convert("L")  # Grayscale
    img       = img.resize((IMG_SIZE, IMG_SIZE))
    arr       = np.array(img, dtype=np.float32) / 255.0
    arr       = 1.0 - arr  # invert: พื้นขาว → 0, เส้นดำ → 1
    return arr


class PredictPayload(BaseModel):
    image: str  # base64 PNG


@router.post("")
async def predict(payload: PredictPayload):
    model = get_model()
    if model is None:
        raise HTTPException(503, "ยังไม่มี model — กรุณาอัปโหลดผ่าน Admin Page")

    arr = preprocess_image(payload.image)

    try:
        # รองรับทั้ง sklearn (flatten), keras/CNN (4D), และ PyTorch (4D)
        if hasattr(model, "predict_proba"):
            # sklearn
            flat = arr.flatten().reshape(1, -1)
            proba = model.predict_proba(flat)[0]
        elif hasattr(model, "forward") or "torch" in str(type(model)):
            # PyTorch CNN
            import torch
            import torch.nn.functional as F
            inp = torch.tensor(arr.reshape(1, 1, IMG_SIZE, IMG_SIZE), dtype=torch.float32)
            with torch.no_grad():
                logits = model(inp)
                proba = F.softmax(logits, dim=1).cpu().numpy()[0]
        else:
            # keras CNN
            inp   = arr.reshape(1, IMG_SIZE, IMG_SIZE, 1)
            proba = model.predict(inp)[0]

        pred_idx    = int(np.argmax(proba))
        confidence  = float(proba[pred_idx])
        all_proba   = {LABELS[i]: round(float(p), 4) for i, p in enumerate(proba)}

    except Exception as e:
        raise HTTPException(500, f"Prediction error: {str(e)}")

    return {
        "prediction":  LABELS[pred_idx],
        "confidence":  confidence,
        "all_proba":   all_proba,
        "model_used":  _model_name,
    }


@router.get("/model-info")
async def model_info():
    return {
        "model_name":   _model_name,
        "model_loaded": _model is not None,
        "labels":       LABELS,
        "img_size":     IMG_SIZE,
    }
