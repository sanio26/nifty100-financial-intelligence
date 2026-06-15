import pandas as pd
from pathlib import Path

# -----------------------------------
# Base Paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FOLDER = BASE_DIR / "data" / "raw"

files = {
    "companies": "companies.xlsx",
    "analysis": "analysis.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "cashflow": "cashflow.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "documents": "documents.xlsx"
}

# -----------------------------------
# Extract Excel → CSV
# -----------------------------------
for table_name, file_name in files.items():

    print("\n" + "=" * 60)
    print(f"Processing: {file_name}")

    file_path = RAW_FOLDER / file_name

    try:
        # Header row is row index 1
        df = pd.read_excel(
            file_path,
            header=1
        )

        # Remove fully empty rows
        df.dropna(how="all", inplace=True)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # Save CSV
        output_path = RAW_FOLDER / f"{table_name}.csv"
        df.to_csv(output_path, index=False)

        print(f"SUCCESS: {table_name}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print("\nColumn Names:")
        print(df.columns.tolist())

    except Exception as e:
        print(f"ERROR processing {file_name}")
        print(e)

print("\nAll files extracted successfully!")