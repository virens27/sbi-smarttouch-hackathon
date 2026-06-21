import pandas as pd
import pickle
import numpy as np

# Load model
with open("../data/model.pkl", "rb") as f:
    model = pickle.load(f)

# Load customer data
df = pd.read_csv("../data/customers.csv")

# Features only
X = df.drop(columns=["customer_id", "is_disengaged"])

# Predict
df["disengagement_probability"] = model.predict_proba(X)[:, 1]
df["predicted_disengaged"] = model.predict(X)

# Generate personalized nudge message
def generate_nudge(row):
    if row["predicted_disengaged"] == 0:
        return "Customer is active. No nudge needed."
    if row["has_investment_product"] == 0:
        return "Hi! Grow your savings with SBI Mutual Funds. Start with just ₹500/month!"
    if row["has_insurance_product"] == 0:
        return "Protect your family today! Explore SBI Life Insurance plans tailored for you."
    if row["mobile_banking_active"] == 0:
        return "Bank smarter! Activate SBI YONO and manage everything from your phone."
    return "We miss you! Log in to SBI Net Banking and explore exclusive offers waiting for you."

df["nudge_message"] = df.apply(generate_nudge, axis=1)

# Show top 10 at-risk customers
at_risk = df[df["predicted_disengaged"] == 1].sort_values(
    "disengagement_probability", ascending=False
).head(10)

print(" Top 10 At-Risk Customers:")
print(at_risk[["customer_id", "disengagement_probability", "nudge_message"]].to_string(index=False))

# Save results
df.to_csv("../data/predictions.csv", index=False)
print("\n Full predictions saved to data/predictions.csv")