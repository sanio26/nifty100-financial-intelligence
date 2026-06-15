import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "data" / "raw"

files = [
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "profitandloss.xlsx",
    "cashflow.xlsx",
    "prosandcons.xlsx",
    "documents.xlsx"
]

for file in files:
    print("\n" + "=" * 80)
    print(f"FILE: {file}")
    print("=" * 80)

    path = RAW_FOLDER / file

    # Read without header
    df = pd.read_excel(path, header=None)

    # Show first 10 rows
    print(df.head(10))