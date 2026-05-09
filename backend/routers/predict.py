"""
Router: /api/predict
ปรับ Preprocessing ให้ตรงกับตอน Train 100% (No Auto-Crop) 
และปรับจูนการ Invert ให้แม่นยำขึ้น
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64, io, os
import numpy as np
from PIL import Image, ImageOps

router = APIRouter()

# ─── Model State ──────────────────────────────────────────────────────────────
_model       = None
_model_name  = "ยังไม่ได้โหลด model"
_model_type  = None

MODELS_DIR   = os.path.join(os.path.dirname(__file__), "..", "..", "models")
LABELS       = ["๒๑", "๒๒", "๒๓", "๒๔", "๒๕"]
IMG_SIZE     = 32

def load_model_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pt":
        import torch
        try:
            model = torch.jit.load(path, map_location="cpu")
        except:
            model = torch.load(path, map_location="cpu", weights_only=False)
        if isinstance(model, dict) or str(type(model)).find("OrderedDict") != -1:
            raise ValueError("State Dict is not supported. Use TorchScript.")
        if hasattr(model, "eval"): model.eval()
        return model, "pytorch"
    elif ext == ".h5":
        from tensorflow.keras.models import load_model as keras_load
        return keras_load(path), "keras"
    elif ext in (".pkl", ".joblib"):
        import joblib
        return joblib.load(path), "sklearn"
    raise ValueError(f"Unsupported format: {ext}")

def get_model():
    global _model, _model_name, _model_type
    if _model is None:
        if not os.path.exists(MODELS_DIR): return None
        files = sorted([f for f in os.listdir(MODELS_DIR) if f.endswith((".pt", ".h5", ".pkl", ".joblib"))])
        if not files: return None
        target = next((f for f in files if "final" in f), files[-1])
        path = os.path.join(MODELS_DIR, target)
        try:
            _model, _model_type = load_model_file(path)
            _model_name = target
        except: return None
    return _model

# ─── Preprocessing (Matching Train Script) ───────────────────────────────────
def preprocess_image(b64_str: str) -> np.ndarray:
    """ต้องตรงกับ load_dataset() ใน train_model.py เป๊ะๆ"""
    try:
        # 1. Load base64
        img_data = b64_str.split(",")[1] if "," in b64_str else b64_str
        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes)).convert("L")
        
        # 2. Resize ทั้งกระดาน (เหมือนตอนโหลด Dataset)
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        
        # 3. Convert to Array & Normalize
        arr = np.array(img, dtype=np.float32) / 255.0
        
        # 4. Invert Logic (ต้องได้พื้นดำ เส้นขาว เหมือนตอน Train)
        # ถ้าค่าเฉลี่ย > 0.5 แสดงว่าเป็นพื้นขาว ให้ Invert
        if np.mean(arr) > 0.5:
            arr = 1.0 - arr
            
        return arr
    except Exception as e:
        raise ValueError(f"Preprocessing error: {str(e)}")

def run_predict(arr: np.ndarray) -> np.ndarray:
    if _model_type == "pytorch":
        import torch
        tensor = torch.tensor(arr).unsqueeze(0).unsqueeze(0) # (1, 1, 32, 32)
        with torch.no_grad():
            out = _model(tensor)
            if isinstance(out, tuple): out = out[0]
            proba = torch.softmax(out, dim=1).numpy()[0]
        return proba
    elif _model_type == "keras":
        inp = arr.reshape(1, IMG_SIZE, IMG_SIZE, 1)
        proba = _model.predict(inp, verbose=0)[0]
        return proba
    elif _model_type == "sklearn":
        flat = arr.flatten().reshape(1, -1)
        proba = _model.predict_proba(flat)[0]
        return proba
    raise ValueError("Unknown model type")

class PredictPayload(BaseModel):
    image: str

@router.post("")
async def predict(payload: PredictPayload):
    model = get_model()
    if model is None: raise HTTPException(503, "Model not loaded")
    
    arr = preprocess_image(payload.image)
    try:
        proba = run_predict(arr)
        pred_idx = int(np.argmax(proba))
        
        # Log ข้อมูลการทำนายลง Terminal เพื่อ Debug
        print(f"--- Prediction Debug ---")
        print(f"Model: {_model_name}")
        print(f"Result: {LABELS[pred_idx]} ({proba[pred_idx]*100:.2f}%)")
        print(f"Mean Pixel Value: {np.mean(arr):.4f}")
        print(f"------------------------")

        return {
            "prediction": LABELS[pred_idx],
            "confidence": float(proba[pred_idx]),
            "all_proba": {LABELS[i]: round(float(p), 4) for i, p in enumerate(proba)},
            "model_used": _model_name
        }
    except Exception as e:
        raise HTTPException(500, f"Predict error: {str(e)}")

@router.get("/model-info")
async def model_info():
    get_model()
    return {
        "model_name": _model_name,
        "model_loaded": _model is not None,
        "labels": LABELS
    }
