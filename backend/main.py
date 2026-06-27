from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

app = FastAPI(title="SBI SmartTouch API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

disengagement_model = None
propensity_model = None
predictions_df = None

PRODUCT_MAP = {
    0: "Mutual Fund",
    1: "Insurance",
    2: "YONO",
    3: "Net Banking"
}

@app.on_event("startup")
def load_models():
    global disengagement_model, propensity_model, predictions_df
    with open("../data/model.pkl", "rb") as f:
        disengagement_model = pickle.load(f)
    with open("../data/propensity_model.pkl", "rb") as f:
        propensity_model = pickle.load(f)
    predictions_df = pd.read_csv("../data/predictions.csv")
    print("Both models and predictions loaded!")

@app.get("/")
def root():
    return {"message": "SBI SmartTouch API v2.0 is running!"}

@app.get("/api/stats")
def get_stats():
    total = len(predictions_df)
    disengaged = int(predictions_df["predicted_disengaged"].sum())
    active = total - disengaged
    product_counts = predictions_df[
        predictions_df["predicted_disengaged"] == 1
    ]["recommended_product"].value_counts().to_dict()
    return {
        "total_customers": total,
        "disengaged": disengaged,
        "active": active,
        "disengagement_rate": round(disengaged / total * 100, 2),
        "product_distribution": product_counts
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
        "recommended_product",
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

@app.get("/api/products/summary")
def get_product_summary():
    disengaged = predictions_df[predictions_df["predicted_disengaged"] == 1]
    summary = disengaged["recommended_product"].value_counts().reset_index()
    summary.columns = ["product", "count"]
    return summary.to_dict(orient="records")