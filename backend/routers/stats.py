"""
Router: /api/stats
แสดงสถิติจำนวน dataset ที่เก็บได้แต่ละ class
"""

from fastapi import APIRouter
import os

router      = APIRouter()
LABELS      = ["๒๑", "๒๒", "๒๓", "๒๔", "๒๕"]
DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dataset")
TARGET      = 50  # จำนวน sample เป้าหมายต่อ class


@router.get("")
async def get_stats():
    """จำนวน sample แต่ละ class + progress"""
    counts = {}
    total  = 0
    for label in LABELS:
        label_dir = os.path.join(DATASET_DIR, label)
        if os.path.exists(label_dir):
            n = len([f for f in os.listdir(label_dir) if f.endswith(".png")])
        else:
            n = 0
        counts[label] = n
        total += n

    return {
        "counts":   counts,
        "total":    total,
        "target":   TARGET,
        "complete": all(v >= TARGET for v in counts.values()),
        "labels":   LABELS,
    }
