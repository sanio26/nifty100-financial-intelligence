import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

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
print("NIFTY100 COMPANY HEALTH SCORE GENERATION")
print("=" * 60)

# ==========================================
# LOAD DATA
# ==========================================
print("\nLoading data from warehouse...")

dim_company = pd.read_sql(
    "SELECT symbol, company_name, roe_percentage, roce_percentage "
    "FROM dim_company",
    engine
)

profit_loss = pd.read_sql(
    """
    SELECT
        symbol,
        year_label,
        net_profit_margin_pct,
        net_profit,
        sales
    FROM fact_profit_loss
    """,
    engine
)

balance_sheet = pd.read_sql(
    """
    SELECT
        symbol,
        debt_to_equity
    FROM fact_balance_sheet
    """,
    engine
)

cashflow = pd.read_sql(
    """
    SELECT
        symbol,
        free_cash_flow
    FROM fact_cash_flow
    """,
    engine
)

analysis = pd.read_sql(
"""
SELECT
company_id AS symbol,
compounded_sales_growth,
compounded_profit_growth,
roe
FROM fact_analysis
""",
engine
)


# ==========================================
# LATEST COMPANY RECORDS
# ==========================================
profit_loss_latest = (
    profit_loss
    .sort_values("year_label")
    .groupby("symbol")
    .tail(1)
)

balance_latest = (
    balance_sheet
    .groupby("symbol")
    .tail(1)
)

cashflow_latest = (
    cashflow
    .groupby("symbol")
    .tail(1)
)

analysis_latest = (
    analysis
    .groupby("symbol")
    .tail(1)
)

# ==========================================
# MERGE DATA
# ==========================================
print("Merging company financial metrics...")

df = dim_company.merge(
    profit_loss_latest,
    on="symbol",
    how="left"
)

df = df.merge(
    balance_latest,
    on="symbol",
    how="left"
)

df = df.merge(
    cashflow_latest,
    on="symbol",
    how="left"
)

df = df.merge(
    analysis_latest,
    on="symbol",
    how="left"
)

# ==========================================
# NULL HANDLING
# ==========================================
numeric_cols = df.select_dtypes(include="number").columns

df[numeric_cols] = df[numeric_cols].fillna(0)
# ==========================================
# CLEAN TEXT PERCENTAGES
# ==========================================
import re

def extract_percentage(value):
    
    if pd.isna(value):
        return 0

    value = str(value)

    # Handles:
    # "TTM: 47%"
    # "10 Years: 11%"
    # "5 Years: 14%"
    # "47%"

    match = re.search(r"(-?\d+\.?\d*)", value)

    if match:
        return float(match.group(1))

    return 0


# Clean analysis columns
df["compounded_sales_growth"] = (
    df["compounded_sales_growth"]
    .apply(extract_percentage)
)

df["compounded_profit_growth"] = (
    df["compounded_profit_growth"]
    .apply(extract_percentage)
)

df["roe"] = (
    df["roe"]
    .apply(extract_percentage)
)

# ==========================================
# SCORING FEATURES
# ==========================================
score_columns = [
"roe_percentage",
"roce_percentage",
"net_profit_margin_pct",
"compounded_sales_growth",
"compounded_profit_growth",
"free_cash_flow",
]


# Debt should reduce score
df["debt_penalty"] = -df["debt_to_equity"]

score_columns.append("debt_penalty")

# ==========================================
# NORMALIZE SCORES
# ==========================================
print("Normalizing financial metrics...")

scaler = MinMaxScaler()

scaled = scaler.fit_transform(df[score_columns])

scaled_df = pd.DataFrame(
    scaled,
    columns=score_columns
)

# ==========================================
# FINAL HEALTH SCORE
# ==========================================
weights = {
"roe_percentage": 0.20,
"roce_percentage": 0.20,
"net_profit_margin_pct": 0.15,
"compounded_sales_growth": 0.15,
"compounded_profit_growth": 0.15,
"free_cash_flow": 0.10,
"debt_penalty": 0.05
}


df["overall_score"] = 0

for col, weight in weights.items():
    df["overall_score"] += scaled_df[col] * weight

df["overall_score"] = (
    df["overall_score"] * 100
).round(2)

# ==========================================
# HEALTH LABEL
# ==========================================
def get_health_label(score):

    if score >= 80:
        return "EXCELLENT"

    elif score >= 65:
        return "GOOD"

    elif score >= 50:
        return "AVERAGE"

    elif score >= 35:
        return "WEAK"

    return "POOR"


df["health_label"] = df[
    "overall_score"
].apply(get_health_label)

# ==========================================
# FINAL OUTPUT TABLE
# ==========================================
output = df[
    [
        "symbol",
        "company_name",
        "overall_score",
        "health_label"
    ]
].copy()

output["computed_at"] = datetime.now()

# ==========================================
# TOP COMPANIES
# ==========================================
print("\nTOP 10 HEALTHIEST COMPANIES")
print(
    output
    .sort_values(
        "overall_score",
        ascending=False
    )
    .head(10)
)

# ==========================================
# SAVE TO DATABASE
# ==========================================
print("\nSaving to PostgreSQL...")

output.to_sql(
    "fact_ml_scores",
    engine,
    if_exists="replace",
    index=False
)

print("\nSUCCESS!")
print("ML Company Health Scores Generated")
print("Saved to table: fact_ml_scores")
print("=" * 60)