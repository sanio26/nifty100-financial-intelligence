import pandas as pd
import numpy as np
from pathlib import Path
import re

# ---------------------------------------
# Paths
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FOLDER = BASE_DIR / "data" / "raw"
CLEAN_FOLDER = BASE_DIR / "data" / "clean"

CLEAN_FOLDER.mkdir(exist_ok=True)

# ---------------------------------------
# Helper Functions
# ---------------------------------------

def standardize_year(year_value):
    """
    Convert:
    Mar-24 -> Mar 2024
    Mar 2024 -> Mar 2024
    TTM -> TTM
    """

    if pd.isna(year_value):
        return None

    year_value = str(year_value).strip()

    if year_value.upper() == "TTM":
        return "TTM"

    match = re.match(r"([A-Za-z]+)[-\s](\d{2,4})", year_value)

    if match:
        month = match.group(1)
        year = match.group(2)

        if len(year) == 2:
            year = f"20{year}"

        return f"{month} {year}"

    return year_value


def extract_fiscal_year(year_value):
    """
    Extract numeric year
    Mar 2024 -> 2024
    Mar-24 -> 2024
    TTM -> NaN
    """

    if pd.isna(year_value):
        return np.nan

    year_value = str(year_value)

    if year_value.upper() == "TTM":
        return np.nan

    match = re.search(r"(\d{2,4})", year_value)

    if match:
        year = match.group(1)

        if len(year) == 2:
            return int("20" + year)

        return int(year)

    return np.nan


def clean_nulls(df):
    """
    Replace NULL text values
    """

    df.replace(
        ["NULL", "Null", "null", ""],
        np.nan,
        inplace=True
    )

    return df


# ---------------------------------------
# Load CSVs
# ---------------------------------------

companies = pd.read_csv(RAW_FOLDER / "companies.csv")
analysis = pd.read_csv(RAW_FOLDER / "analysis.csv")
balancesheet = pd.read_csv(RAW_FOLDER / "balancesheet.csv")
profitloss = pd.read_csv(RAW_FOLDER / "profitandloss.csv")
cashflow = pd.read_csv(RAW_FOLDER / "cashflow.csv")
proscons = pd.read_csv(RAW_FOLDER / "prosandcons.csv")
documents = pd.read_csv(RAW_FOLDER / "documents.csv")

# ---------------------------------------
# Clean NULLS
# ---------------------------------------

datasets = [
    companies,
    analysis,
    balancesheet,
    profitloss,
    cashflow,
    proscons,
    documents
]

for df in datasets:
    clean_nulls(df)

# ---------------------------------------
# Clean Company Names
# ---------------------------------------

companies["company_name"] = (
    companies["company_name"]
    .astype(str)
    .str.strip()
    .str.replace(r"\r|\n", "", regex=True)
)

# ---------------------------------------
# Standardize Years
# ---------------------------------------

year_tables = [
    balancesheet,
    profitloss,
    cashflow,
    documents
]

for df in year_tables:
    df["year_label"] = df["year"].apply(
        standardize_year
    )

    df["fiscal_year"] = df["year"].apply(
        extract_fiscal_year
    )

# ---------------------------------------
# Financial Computed Columns
# ---------------------------------------

# Convert numeric columns safely
numeric_cols_profit = [
    "sales",
    "expenses",
    "operating_profit",
    "interest",
    "net_profit"
]

for col in numeric_cols_profit:
    profitloss[col] = pd.to_numeric(
        profitloss[col],
        errors="coerce"
    )

profitloss["net_profit_margin_pct"] = (
    profitloss["net_profit"]
    / profitloss["sales"]
) * 100

profitloss["expense_ratio_pct"] = (
    profitloss["expenses"]
    / profitloss["sales"]
) * 100

profitloss["interest_coverage"] = (
    profitloss["operating_profit"]
    / profitloss["interest"]
)

# ---------------------------------------
# Balance Sheet Metrics
# ---------------------------------------

numeric_cols_bs = [
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets"
]

for col in numeric_cols_bs:
    balancesheet[col] = pd.to_numeric(
        balancesheet[col],
        errors="coerce"
    )

balancesheet["debt_to_equity"] = (
    balancesheet["borrowings"]
    /
    (
        balancesheet["equity_capital"]
        + balancesheet["reserves"]
    )
)

balancesheet["equity_ratio"] = (
    (
        balancesheet["equity_capital"]
        + balancesheet["reserves"]
    )
    /
    balancesheet["total_assets"]
)

# ---------------------------------------
# Cash Flow Metrics
# ---------------------------------------

cashflow["operating_activity"] = pd.to_numeric(
    cashflow["operating_activity"],
    errors="coerce"
)

cashflow["investing_activity"] = pd.to_numeric(
    cashflow["investing_activity"],
    errors="coerce"
)

cashflow["free_cash_flow"] = (
    cashflow["operating_activity"]
    +
    cashflow["investing_activity"]
)

# ---------------------------------------
# Save Clean Files
# ---------------------------------------

companies.to_csv(
    CLEAN_FOLDER / "companies_clean.csv",
    index=False
)

analysis.to_csv(
    CLEAN_FOLDER / "analysis_clean.csv",
    index=False
)

balancesheet.to_csv(
    CLEAN_FOLDER / "balancesheet_clean.csv",
    index=False
)

profitloss.to_csv(
    CLEAN_FOLDER / "profitandloss_clean.csv",
    index=False
)

cashflow.to_csv(
    CLEAN_FOLDER / "cashflow_clean.csv",
    index=False
)

proscons.to_csv(
    CLEAN_FOLDER / "prosandcons_clean.csv",
    index=False
)

documents.to_csv(
    CLEAN_FOLDER / "documents_clean.csv",
    index=False
)

print("\nSUCCESS: Clean files saved!")
print("Location: data/clean/")