import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 1000

data = pd.DataFrame({
    "customer_id": [f"CUST{str(i).zfill(4)}" for i in range(1, n+1)],
    "age": np.random.randint(18, 65, n),
    "monthly_transactions": np.random.randint(0, 50, n),
    "avg_transaction_amount": np.round(np.random.uniform(100, 50000, n), 2),
    "login_frequency_per_month": np.random.randint(0, 30, n),
    "num_products_used": np.random.randint(1, 8, n),
    "days_since_last_transaction": np.random.randint(0, 180, n),
    "salary_credited_last_month": np.random.randint(0, 2, n),
    "has_investment_product": np.random.randint(0, 2, n),
    "has_insurance_product": np.random.randint(0, 2, n),
    "mobile_banking_active": np.random.randint(0, 2, n),
    "customer_tenure_years": np.random.randint(1, 20, n),
})

# Generate target: 1 = disengaged, 0 = active
data["is_disengaged"] = (
    (data["days_since_last_transaction"] > 60) |
    (data["login_frequency_per_month"] < 3) |
    (data["monthly_transactions"] < 5)
).astype(int)

# Save to data folder
os.makedirs("../data", exist_ok=True)
data.to_csv("../data/customers.csv", index=False)
print(f"    Dataset generated: {n} customers saved to data/customers.csv")
print(f"   Disengaged: {data['is_disengaged'].sum()} | Active: {(data['is_disengaged']==0).sum()}")