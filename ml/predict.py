import pandas as pd
import pickle
import numpy as np

# Load both models
with open("../data/model.pkl", "rb") as f:
    disengagement_model = pickle.load(f)

with open("../data/propensity_model.pkl", "rb") as f:
    propensity_model = pickle.load(f)

# Product label map
PRODUCT_MAP = {
    0: ("Mutual Fund", "Grow your savings with SBI Mutual Funds. Start with just Rs.500/month!"),
    1: ("Insurance", "Protect your family today! Explore SBI Life Insurance plans tailored for you."),
    2: ("YONO", "Bank smarter! Activate SBI YONO and manage everything from your phone."),
    3: ("Net Banking", "We miss you! Log in to SBI Net Banking and explore exclusive offers waiting for you.")
}

# Load data
df = pd.read_csv("../data/customers.csv")
X = df.drop(columns=["customer_id", "is_disengaged"])

# Predict disengagement
df["disengagement_probability"] = disengagement_model.predict_proba(X)[:, 1]
df["predicted_disengaged"] = disengagement_model.predict(X)

# Predict recommended product using propensity model
product_preds = propensity_model.predict(X)
df["recommended_product"] = [PRODUCT_MAP[p][0] for p in product_preds]
df["nudge_message"] = [PRODUCT_MAP[p][1] for p in product_preds]

# For active customers, override nudge
df.loc[df["predicted_disengaged"] == 0, "nudge_message"] = "Customer is active. No nudge needed."
df.loc[df["predicted_disengaged"] == 0, "recommended_product"] = "None"

# Show top 10 at-risk
at_risk = df[df["predicted_disengaged"] == 1].sort_values(
    "disengagement_probability", ascending=False
).head(10)

print("Top 10 At-Risk Customers with ML-Recommended Products:")
print(at_risk[["customer_id", "disengagement_probability", "recommended_product", "nudge_message"]].to_string(index=False))

# Save
df.to_csv("../data/predictions.csv", index=False)
print("\nFull predictions saved to data/predictions.csv")