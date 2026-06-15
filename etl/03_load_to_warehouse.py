
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# ==========================================
# DATABASE CONFIG
# ==========================================

DB_USER = "postgres"
DB_PASSWORD = "sanio23"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100_dw"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_FOLDER = BASE_DIR / "data" / "clean"

# ==========================================
# READ FILES
# ==========================================

print("Reading clean CSV files...")

companies = pd.read_csv(
    CLEAN_FOLDER / "companies_clean.csv"
)

analysis = pd.read_csv(
    CLEAN_FOLDER / "analysis_clean.csv"
)

balancesheet = pd.read_csv(
    CLEAN_FOLDER / "balancesheet_clean.csv"
)

profitloss = pd.read_csv(
    CLEAN_FOLDER / "profitandloss_clean.csv"
)

cashflow = pd.read_csv(
    CLEAN_FOLDER / "cashflow_clean.csv"
)

proscons = pd.read_csv(
    CLEAN_FOLDER / "prosandcons_clean.csv"
)

documents = pd.read_csv(
    CLEAN_FOLDER / "documents_clean.csv"
)

# ==========================================
# PREPARE DIM COMPANY
# ==========================================

print("Preparing dim_company...")

dim_company = companies.rename(
    columns={
        "id": "symbol",
        "nse_profile": "nse_url",
        "bse_profile": "bse_url"
    }
)

# Keep only valid columns
dim_company = dim_company[
    [
        "symbol",
        "company_name",
        "company_logo",
        "website",
        "nse_url",
        "bse_url",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage",
        "about_company"
    ]
].copy()

# ==========================================
# ADD MISSING SYMBOLS
# ==========================================

all_symbols = pd.concat([
    profitloss["company_id"],
    balancesheet["company_id"],
    cashflow["company_id"],
    analysis["company_id"],
    proscons["company_id"],
    documents["company_id"]
]).dropna().unique()

existing_symbols = set(
    dim_company["symbol"]
)

missing_symbols = [
    symbol
    for symbol in all_symbols
    if symbol not in existing_symbols
]

print(
    f"Missing companies found: "
    f"{len(missing_symbols)}"
)

if len(missing_symbols) > 0:

    missing_df = pd.DataFrame({
        "symbol": missing_symbols,
        "company_name": missing_symbols,
        "company_logo": None,
        "website": None,
        "nse_url": None,
        "bse_url": None,
        "face_value": None,
        "book_value": None,
        "roce_percentage": None,
        "roe_percentage": None,
        "about_company": None
    })

    dim_company = pd.concat(
        [dim_company, missing_df],
        ignore_index=True
    )

# Remove duplicates
dim_company.drop_duplicates(
    subset=["symbol"],
    inplace=True
)

# ==========================================
# PREPARE FACT TABLES
# ==========================================

print("Preparing fact tables...")

# ---------- PROFIT & LOSS ----------

profitloss.rename(
    columns={"company_id": "symbol"},
    inplace=True
)

profitloss = profitloss[
    [
        "symbol",
        "year_label",
        "sales",
        "expenses",
        "operating_profit",
        "opm_percentage",
        "other_income",
        "interest",
        "depreciation",
        "profit_before_tax",
        "tax_percentage",
        "net_profit",
        "eps",
        "dividend_payout",
        "net_profit_margin_pct",
        "expense_ratio_pct",
        "interest_coverage"
    ]
].copy()

# Replace infinity values
profitloss.replace(
    [float("inf"), -float("inf")],
    None,
    inplace=True
)

# ---------- BALANCE SHEET ----------

balancesheet.rename(
    columns={"company_id": "symbol"},
    inplace=True
)

balancesheet = balancesheet[
    [
        "symbol",
        "year_label",
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
        "total_liabilities",
        "fixed_assets",
        "cwip",
        "investments",
        "other_asset",
        "total_assets",
        "debt_to_equity",
        "equity_ratio"
    ]
].copy()

# ---------- CASH FLOW ----------

cashflow.rename(
    columns={"company_id": "symbol"},
    inplace=True
)

cashflow = cashflow[
    [
        "symbol",
        "year_label",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
        "free_cash_flow"
    ]
].copy()

# ---------- ANALYSIS ----------

analysis = analysis[
    [
        "id",
        "company_id",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]
].copy()

# ---------- PROS & CONS ----------

proscons = proscons[
    [
        "id",
        "company_id",
        "pros",
        "cons"
    ]
].copy()

# ---------- DOCUMENTS ----------

documents = documents[
    [
        "id",
        "company_id",
        "year",
        "annual_report"
    ]
].copy()

# ==========================================
# CLEAR OLD DATA (SAFE RELOAD)
# ==========================================

print("Clearing old tables...")

with engine.begin() as conn:

    conn.execute(
        text(
            "TRUNCATE TABLE "
            "fact_profit_loss, "
            "fact_balance_sheet, "
            "fact_cash_flow, "
            "fact_analysis, "
            "fact_pros_cons, "
            "fact_documents, "
            "dim_company "
            "CASCADE"
        )
    )

# ==========================================
# LOAD TABLES
# ==========================================

try:

    print("Loading dim_company...")

    dim_company.to_sql(
        "dim_company",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_profit_loss...")

    profitloss.to_sql(
        "fact_profit_loss",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_balance_sheet...")

    balancesheet.to_sql(
        "fact_balance_sheet",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_cash_flow...")

    cashflow.to_sql(
        "fact_cash_flow",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_analysis...")

    analysis.to_sql(
        "fact_analysis",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_pros_cons...")

    proscons.to_sql(
        "fact_pros_cons",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Loading fact_documents...")

    documents.to_sql(
        "fact_documents",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(
        "\nSUCCESS: "
        "Data Warehouse Loaded Successfully!"
    )

except Exception as e:

    print("\nERROR:")
    print(str(e))

