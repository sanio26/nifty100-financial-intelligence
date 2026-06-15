import pandas as pd
from sqlalchemy import create_engine

# ==============================
# DATABASE CONNECTION
# ==============================
DB_USER = "postgres"
DB_PASSWORD = "sanio23"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100_dw"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("=" * 60)
print("RUNNING DATA QUALITY CHECKS")
print("=" * 60)

# ==============================
# LOAD TABLES
# ==============================
dim_company = pd.read_sql("SELECT * FROM dim_company", engine)

fact_profit_loss = pd.read_sql(
    "SELECT * FROM fact_profit_loss", engine
)

fact_balance_sheet = pd.read_sql(
    "SELECT * FROM fact_balance_sheet", engine
)

fact_cash_flow = pd.read_sql(
    "SELECT * FROM fact_cash_flow", engine
)

fact_analysis = pd.read_sql(
    "SELECT * FROM fact_analysis", engine
)

fact_documents = pd.read_sql(
    "SELECT * FROM fact_documents", engine
)

fact_pros_cons = pd.read_sql(
    "SELECT * FROM fact_pros_cons", engine
)

# ==============================
# 1. ROW COUNTS
# ==============================
print("\n1. TABLE ROW COUNTS")

tables = {
    "dim_company": dim_company,
    "fact_profit_loss": fact_profit_loss,
    "fact_balance_sheet": fact_balance_sheet,
    "fact_cash_flow": fact_cash_flow,
    "fact_analysis": fact_analysis,
    "fact_documents": fact_documents,
    "fact_pros_cons": fact_pros_cons,
}

for name, df in tables.items():
    print(f"{name}: {len(df)} rows")

# ==============================
# 2. MISSING COMPANIES
# ==============================
print("\n2. FOREIGN KEY CHECKS")

company_symbols = set(dim_company["symbol"])

fact_tables = {
    "fact_profit_loss": fact_profit_loss,
    "fact_balance_sheet": fact_balance_sheet,
    "fact_cash_flow": fact_cash_flow,
    "fact_analysis": fact_analysis,
    "fact_documents": fact_documents,
    "fact_pros_cons": fact_pros_cons,
}

for table_name, df in fact_tables.items():

    if "symbol" in df.columns:
        fact_symbols = set(df["symbol"].dropna())

    elif "company_id" in df.columns:
        fact_symbols = set(df["company_id"].dropna())

    else:
        continue

    missing = fact_symbols - company_symbols

    print(f"\n{table_name}")

    if len(missing) == 0:
        print("✓ No missing companies")
    else:
        print(f"✗ Missing companies: {missing}")

# ==============================
# 3. NULL VALUE CHECKS
# ==============================
print("\n3. NULL VALUE CHECKS")

critical_columns = {
    "fact_profit_loss": ["sales", "net_profit"],
    "fact_balance_sheet": ["total_assets"],
    "fact_cash_flow": ["operating_activity"],
}

for table_name, cols in critical_columns.items():

    df = tables[table_name]

    print(f"\n{table_name}")

    for col in cols:
        null_count = df[col].isnull().sum()
        print(f"{col}: {null_count} null values")

# ==============================
# 4. DUPLICATE CHECKS
# ==============================
print("\n4. DUPLICATE CHECKS")

duplicate_checks = {
    "fact_profit_loss": ["symbol", "year_label"],
    "fact_balance_sheet": ["symbol", "year_label"],
    "fact_cash_flow": ["symbol", "year_label"],
}

for table_name, cols in duplicate_checks.items():

    df = tables[table_name]

    duplicates = df.duplicated(subset=cols).sum()

    print(f"{table_name}: {duplicates} duplicates")

# ==============================
# 5. DATA QUALITY SUMMARY
# ==============================
print("\n" + "=" * 60)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 60)