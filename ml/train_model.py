import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Load data
df = pd.read_csv("../data/customers.csv")

# Features and target
X = df.drop(columns=["customer_id", "is_disengaged"])
y = df["is_disengaged"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"  Model trained successfully!")
print(f"   Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("../data", exist_ok=True)
with open("../data/model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Model saved to data/model.pkl")