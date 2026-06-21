# SBI SmartTouch

**Agentic AI Customer Engagement Engine for SBI Digital Banking**

Built for SBI AI Online Hackathon @ GFF 2026

---

## Problem Statement

**Digital Engagement** — Create AI-driven engagement models that
proactively interact with customers based on behaviours, financial
patterns, and life events.

---

## Solution

SBI SmartTouch is an Agentic AI system that:
- Monitors customer financial behavior patterns continuously
- Predicts disengagement before it happens (99.5% accuracy)
- Automatically generates personalized nudge messages
- Delivers the right message at the right time via the right channel

---

## Architecture
Customer Data -> ML Pipeline -> Prediction Engine -> Agentic Nudge Layer -> Dashboard

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| ML/AI      | Python, scikit-learn, Random Forest |
| Backend    | FastAPI, uvicorn                    |
| Frontend   | Next.js, React, Tailwind CSS        |
| Data       | pandas, NumPy                       |
| Deployment | Docker-ready                        |

---

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### ML Pipeline
```bash
cd ml
python generate_data.py
python train_model.py
python predict.py
```

---

## API Endpoints

| Endpoint               | Description                       |
|------------------------|-----------------------------------|
| GET /api/stats         | Overall engagement statistics     |
| GET /api/at-risk       | Top at-risk customers with nudges |
| GET /api/customer/{id} | Individual customer profile       |
| GET /docs              | Interactive API documentation     |

---

## Team

**Team ZeroGap**

| Member | Name | Role |
|--------|------|------|
| Member 1 | [Full Name] | [Role] |
| Member 2 | [Full Name] | [Role] |

---

## License

MIT