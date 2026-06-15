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
print("NIFTY100 COMPANY PERFORMANCE ANALYSIS")
print("=" * 60)

# ==========================================
# LOAD COMPANY DATA
# ==========================================
query = """
SELECT
    symbol,
    company_name,
    roe_percentage,
    roce_percentage
FROM dim_company
"""

company_df = pd.read_sql(query, engine)

# ==========================================
# LOAD PROFIT & SALES DATA
# ==========================================
profit_query = """
SELECT
    symbol,
    sales,
    net_profit
FROM fact_profit_loss
"""

profit_df = pd.read_sql(profit_query, engine)

# ==========================================
# GET LATEST RECORDS ONLY
# ==========================================
profit_df = (
    profit_df
    .groupby("symbol")
    .tail(1)
)

# ==========================================
# MERGE DATA
# ==========================================
merged_df = profit_df.merge(
    company_df,
    on="symbol",
    how="left"
)

# ==========================================
# TOP COMPANIES ANALYSIS
# ==========================================
top_sales = (
    merged_df
    .sort_values("sales", ascending=False)
    .head(10)
)

top_profit = (
    merged_df
    .sort_values("net_profit", ascending=False)
    .head(10)
)

top_roe = (
    merged_df
    .sort_values("roe_percentage", ascending=False)
    .head(10)
)

# ==========================================
# PRINT RESULTS
# ==========================================
print("\nTop Companies by Sales")
print(top_sales[["company_name", "sales"]])

print("\nTop Companies by Profit")
print(top_profit[["company_name", "net_profit"]])

print("\nTop Companies by ROE")
print(top_roe[["company_name", "roe_percentage"]])

# ==========================================
# VISUALIZATION 1 - SALES
# ==========================================
plt.figure(figsize=(10, 6))

plt.bar(
    top_sales["company_name"],
    top_sales["sales"]
)

plt.title("Top Companies by Sales")
plt.xlabel("Company")
plt.ylabel("Sales")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 2 - NET PROFIT
# ==========================================
plt.figure(figsize=(10, 6))

plt.bar(
    top_profit["company_name"],
    top_profit["net_profit"]
)

plt.title("Top Companies by Net Profit")
plt.xlabel("Company")
plt.ylabel("Net Profit")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 3 - ROE
# ==========================================
plt.figure(figsize=(10, 6))

plt.bar(
    top_roe["company_name"],
    top_roe["roe_percentage"]
)

plt.title("Top Companies by ROE")
plt.xlabel("Company")
plt.ylabel("ROE %")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

print("\nSUCCESS!")
print("Company performance analysis completed")
print("=" * 60)