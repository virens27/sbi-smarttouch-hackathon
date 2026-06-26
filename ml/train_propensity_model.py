import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

# Load data
df = pd.read_csv("../data/customers.csv")

# Define product labels
# 0 = Mutual Fund, 1 = Insurance, 2 = YONO, 3 = Net Banking
def assign_product(row):
    if row["has_investment_product"] == 0:
        return 0  # Mutual Fund
    if row["has_insurance_product"] == 0:
        return 1  # Insurance
    if row["mobile_banking_active"] == 0:
        return 2  # YONO
    return 3      # Net Banking

df["recommended_product"] = df.apply(assign_product, axis=1)

# Features
X = df.drop(columns=["customer_id", "is_disengaged", "recommended_product"])
y = df["recommended_product"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Product Propensity Model trained!")
print(f"Accuracy: {model.score(X_test, y_test)*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=[
    "Mutual Fund", "Insurance", "YONO", "Net Banking"
]))

# Save
os.makedirs("../data", exist_ok=True)
with open("../data/propensity_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Propensity model saved to data/propensity_model.pkl")