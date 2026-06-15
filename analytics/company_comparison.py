import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# ==========================================
# DATABASE CONNECTION
# ==========================================
DB_USER = "postgres"
DB_PASSWORD = "sanio23"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100_dw"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("=" * 60)
print("NIFTY100 COMPANY COMPARISON ANALYSIS")
print("=" * 60)

# ==========================================
# SELECT COMPANIES TO COMPARE
# ==========================================
companies = [
    "TCS",
    "INFY",
    "WIPRO"
]

print(f"\nComparing: {companies}")

# ==========================================
# LOAD DATA
# ==========================================
query = f"""
SELECT
    symbol,
    sales,
    net_profit,
    net_profit_margin_pct
FROM fact_profit_loss
WHERE symbol IN ({",".join([f"'{c}'" for c in companies])})
"""

profit_loss = pd.read_sql(query, engine)

health_scores = pd.read_sql(
    """
    SELECT
        symbol,
        overall_score,
        health_label
    FROM fact_ml_scores
    """,
    engine
)

dim_company = pd.read_sql(
    """
    SELECT
        symbol,
        roe_percentage,
        roce_percentage
    FROM dim_company
    """,
    engine
)

# ==========================================
# LATEST RECORDS ONLY
# ==========================================
comparison = (
    profit_loss
    .groupby("symbol")
    .tail(1)
)

# Merge with company metrics
comparison = comparison.merge(
    dim_company,
    on="symbol",
    how="left"
)

comparison = comparison.merge(
    health_scores,
    on="symbol",
    how="left"
)

# ==========================================
# PRINT RESULTS
# ==========================================
print("\nCOMPANY COMPARISON")
print(comparison)

# ==========================================
# VISUALIZATION
# ==========================================

# Revenue Comparison
plt.figure(figsize=(8, 5))
plt.bar(
    comparison["symbol"],
    comparison["sales"]
)
plt.title("Revenue Comparison")
plt.xlabel("Company")
plt.ylabel("Sales")
plt.show()

# Profit Comparison
plt.figure(figsize=(8, 5))
plt.bar(
    comparison["symbol"],
    comparison["net_profit"]
)
plt.title("Net Profit Comparison")
plt.xlabel("Company")
plt.ylabel("Net Profit")
plt.show()

# Health Score Comparison
plt.figure(figsize=(8, 5))
plt.bar(
    comparison["symbol"],
    comparison["overall_score"]
)
plt.title("ML Health Score Comparison")
plt.xlabel("Company")
plt.ylabel("Health Score")
plt.show()

print("\nSUCCESS!")
print("Company comparison completed")
print("=" * 60)