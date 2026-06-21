from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

app = FastAPI(title="SBI SmartTouch API", version="1.0.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and predictions on startup
model = None
predictions_df = None

@app.on_event("startup")
def load_model():
    global model, predictions_df
    with open("../data/model.pkl", "rb") as f:
        model = pickle.load(f)
    predictions_df = pd.read_csv("../data/predictions.csv")
    print(" Model and predictions loaded!")

@app.get("/")
def root():
    return {"message": "SBI SmartTouch API is running!"}

@app.get("/api/stats")
def get_stats():
    total = len(predictions_df)
    disengaged = int(predictions_df["predicted_disengaged"].sum())
    active = total - disengaged
    return {
        "total_customers": total,
        "disengaged": disengaged,
        "active": active,
        "disengagement_rate": round(disengaged / total * 100, 2)
    }

@app.get("/api/at-risk")
def get_at_risk(limit: int = 10):
    at_risk = predictions_df[
        predictions_df["predicted_disengaged"] == 1
    ].sort_values("disengagement_probability", ascending=False).head(limit)
    return at_risk[[
        "customer_id",
        "age",
        "disengagement_probability",
        "nudge_message"
    ]].to_dict(orient="records")

@app.get("/api/customer/{customer_id}")
def get_customer(customer_id: str):
    customer = predictions_df[
        predictions_df["customer_id"] == customer_id
    ]
    if customer.empty:
        return {"error": "Customer not found"}
    return customer.to_dict(orient="records")[0]