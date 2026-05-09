# Thai Digit Classifier · ๒๑–๒๕
**AIE322 Supervised ML (2/2568)**

ระบบ Web App สำหรับ classify ลายมือเขียนเลขไทย ๒๑–๒๕

---

## โครงสร้างโปรเจค

```
thai-digit-collector/
├── backend/
│   ├── main.py                  # FastAPI app หลัก + serve frontend
│   ├── requirements.txt
│   └── routers/
│       ├── collect.py           # POST /api/collect/save-sample
│       ├── predict.py           # POST /api/predict
│       ├── admin.py             # POST /api/admin/upload-model
│       └── stats.py             # GET  /api/stats
├── frontend/
│   ├── collect.html             # หน้าเก็บ dataset
│   ├── user.html                # หน้า User (Predict)
│   └── admin.html               # หน้า Admin (Upload Model)
├── dataset/
│   ├── ๒๑/                      # PNG แยกตาม class
│   ├── ๒๒/
│   ├── ๒๓/
│   ├── ๒๔/
│   └── ๒๕/
├── models/                      # เก็บ model ที่ train แล้ว
└── train/
    └── train_model.py           # (สร้างเอง) script สำหรับ train โมเดล
```

---

## วิธีติดตั้งและรัน

### 1. ติดตั้ง dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. รัน server
```bash
cd backend
python main.py
# หรือ
uvicorn main:app --reload --port 8000
```

### 3. เปิดเว็บ
| หน้า | URL |
|---|---|
| เก็บ Dataset | http://localhost:8000/collect |
| Predict (User) | http://localhost:8000/ |
| Admin | http://localhost:8000/admin |

---

## API Endpoints

| Method | Path | คำอธิบาย |
|---|---|---|
| POST | `/api/collect/save-sample` | บันทึก canvas image + label |
| DELETE | `/api/collect/delete-last/{label}` | ลบรูปล่าสุดของ label |
| POST | `/api/predict` | ทำนายเลขจาก canvas image |
| GET | `/api/predict/model-info` | ดู model ที่โหลดอยู่ |
| POST | `/api/admin/upload-model` | อัปโหลด model ใหม่ (hot-reload) |
| GET | `/api/admin/models` | ดูรายการ model ทั้งหมด |
| DELETE | `/api/admin/models/{filename}` | ลบ model |
| GET | `/api/stats` | จำนวน sample แต่ละ class |

---

## Flow การใช้งาน

### ขั้นตอนที่ 1 — เก็บ Dataset
1. เปิด `/collect`
2. เลือก label (๒๑–๒๕)
3. เขียนเลขไทยใน canvas
4. กด **บันทึก** → ไฟล์จะถูกเก็บใน `dataset/{label}/`
5. ทำซ้ำจนได้อย่างน้อย 50 รูป/class

### ขั้นตอนที่ 2 — Train Model
```bash
cd train
python train_model.py
# model จะถูก save เป็น .pkl หรือ .h5 ใน models/
```

### ขั้นตอนที่ 3 — อัปโหลด Model
1. เปิด `/admin`
2. อัปโหลดไฟล์ model
3. ระบบ hot-reload โดยไม่ต้อง restart server

### ขั้นตอนที่ 4 — ทดสอบ Predict
1. เปิด `/` (User Page)
2. เขียนเลขไทย
3. กด **ทำนาย**

---

## Format ไฟล์ Dataset

```
dataset/
  ๒๑/
    21_001_20250501_153012.png
    21_002_20250501_153045.png
    ...
  ๒๒/
    22_001_...png
    ...
```

---

## Extra Points Checklist

- [x] ระบบเก็บ dataset ผ่านเว็บ (`/collect` + `/api/collect/save-sample`)
- [x] Hot-reload model โดยไม่ restart server (`/api/admin/upload-model`)
- [ ] Cross-validation (ทำใน `train_model.py`)
- [ ] Error analysis / Confusion matrix visualization

---

## สมาชิกในทีม

| ชื่อ-สกุล | รหัสนักศึกษา | ส่วนที่รับผิดชอบ |
|---|---|---|
| ... | ... | ... |
