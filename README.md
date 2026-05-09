# 🇹🇭 Thai Digit Intelligence · ๒๑–๒๕
**AIE322 Supervised Machine Learning Project (2/2568)**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/ML-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Modern UI](https://img.shields.io/badge/Frontend-Vanilla_CSS_3-264de4?style=for-the-badge&logo=css3&logoColor=white)](#)

---

## 🏛️ Project Overview
**Thai Digit Intelligence** คือระบบนิเวศน์สำหรับการเก็บข้อมูล (Data Collection) และการประมวลผลลายมือเขียนตัวเลขไทย (Handwriting Recognition) โดยเน้นไปที่ช่วงตัวเลข **๒๑ ถึง ๒๕** โปรเจคนี้สร้างขึ้นเพื่อประยุกต์ใช้ความรู้ด้าน **Supervised Learning** ตั้งแต่ต้นน้ำ (Data Collection) กลางน้ำ (Model Training) ไปจนถึงปลายน้ำ (Model Deployment & Inference)

### 🌟 Key Highlights
- **Real-time Drawing Pad**: แผ่นวาดเขียนระบบสัมผัสที่รองรับทั้ง Mouse และ Touch events
- **Interactive Dataset Collector**: ระบบจัดเก็บภาพลายมือแบบแยก Class อัตโนมัติ เพื่อสร้าง Dataset คุณภาพสูง
- **Neural Inference Engine**: ใช้ Convolutional Neural Networks (CNN) บน PyTorch เพื่อการทำนายที่แม่นยำสูง (>99%)
- **MLOps Friendly**: ระบบ Admin Dashboard สำหรับการอัปโหลดและสลับโมเดลแบบ Hot-Reload โดยไม่ต้องปิด Server

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5 (Semantic), Vanilla CSS (Modern Glassmorphism), JavaScript (Canvas API) |
| **Backend** | Python 3.14+, FastAPI, Uvicorn |
| **Machine Learning** | PyTorch (Core Engine), Scikit-learn (Metrics/CV), NumPy, Pillow |
| **Data Viz** | Matplotlib, Seaborn |

---

## 🧠 Machine Learning Architecture (Academic Bridge)

ในเชิงวิชาการ โปรเจคนี้ใช้สถาปัตยกรรม **Deep Learning** แบบ **Convolutional Neural Networks (CNN)** ซึ่งมีความสามารถในการสกัดคุณลักษณะ (Feature Extraction) จากภาพลายมือได้ดีกว่า Multi-layer Perceptron (MLP) แบบดั้งเดิม

### 🔬 Theoretical Implementation
1. **Feature Extraction Layer**: ประกอบด้วย 3 Conv Blocks (Convolution -> BatchNorm -> ReLU -> MaxPool) เพื่อเรียนรู้ Patterns ของเส้นสายเลขไทยที่มีความโค้งมนเฉพาะตัว
2. **Data Augmentation**: มีการใช้ Random Rotation, Scaling และ Translation เพื่อให้โมเดลมีความทนทาน (Robustness) ต่อสไตล์การเขียนที่หลากหลาย
3. **Validation Strategy**: ใช้ **5-Fold Cross-Validation** เพื่อยืนยันว่าโมเดลไม่เกิดการ Overfitting และมี Generalization Error ที่ต่ำ
4. **Optimization**: ใช้ Adam Optimizer พร้อมกับ Learning Rate Scheduler (ReduceLROnPlateau) เพื่อการลู่เข้าของ Loss ที่มีประสิทธิภาพ

---

## 📁 Project Structure

```bash
thai-digit-collector/
├── backend/
│   ├── main.py                  # API Entry Point & Frontend Hosting
│   ├── requirements.txt         # Production dependencies
│   └── routers/                 # Modular API Routes
│       ├── collect.py           # Dataset Acquisition Logic
│       ├── predict.py           # Model Inference Service
│       ├── admin.py             # Model Management & Hot-Reload
│       └── stats.py             # Data Insights & Analytics
├── frontend/
│   ├── collect.html             # High-fidelity Collection Interface
│   ├── user.html                # Predictive "Magic Pad" UI
│   └── admin.html               # ML Management Dashboard
├── dataset/
│   └── ๒๑–๒๕/                  # PNG Samples (400 samples/class)
├── models/
│   ├── train_model.py           # Core Training Pipeline (PyTorch)
│   ├── model_cnn_final.pt       # Production Traced Model (TorchScript)
│   └── *_report.txt             # Auto-generated Training Logs
└── scratch/                     # Development Utility Scripts
```

---

## 🚀 Getting Started

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/USER/Thai-digit-collector.git
cd Thai-digit-collector

# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows

# Install Dependencies
cd backend
pip install -r requirements.txt
```

### 2. Execution
```bash
python main.py
```
Server จะทำงานที่ `http://localhost:8000`

---

## 📊 Performance Report

จากการทดสอบบน Dataset จำนวน 2,000 รูป (400 รูปต่อ Class) ผลลัพธ์ที่ได้มีความแม่นยำดังนี้:

| Metric | Score |
| :--- | :--- |
| **Test Accuracy** | 99.00% |
| **Weighted F1-Score** | 0.99 |
| **CV Mean Accuracy** | 99.70% ± 0.19% |

> [!TIP]
> รายงานฉบับเต็มและ Confusion Matrix สามารถดูได้ที่ [training_report.txt](file:///d:/Thai-digit-collector/models/training_report.txt) และภาพกราฟในโฟลเดอร์ `models/`

---

## 👥 สมาชิกในทีม

| ชื่อ-สกุล | รหัสนักศึกษา | ส่วนที่รับผิดชอบ |
|---|---|---|
| ... | ... | ... |

---

<div align="center">
  <p><i>This project is part of the AIE322 Supervised Learning Course.</i></p>
  <p>&copy; 2026 AI Thai Digit Predictor Group</p>
</div>
