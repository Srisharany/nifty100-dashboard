import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

print("✅ RUNNING UPDATED FILE")

# -------------------------------
# 1. DB CONNECTION (FIXED)
# -------------------------------
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Pinky1509@",   # keep your real password
    host="localhost",
    port=5432,
    database="nifty_warehouse"
)

engine = create_engine(url)

# -------------------------------
# 2. PATH
# -------------------------------
CLEAN_PATH = r'D:\BLUESTOCK\Task2\nifty_project\data\clean'

# -------------------------------
# 3. LOAD FILES
# -------------------------------

# FIX: skip first bad header row
companies = pd.read_csv(
    os.path.join(CLEAN_PATH, "companies.csv"),
    skiprows=1
)

balancesheet = pd.read_csv(os.path.join(CLEAN_PATH, "balancesheet.csv"))
profit = pd.read_csv(os.path.join(CLEAN_PATH, "profit.csv"))
cashflow = pd.read_csv(os.path.join(CLEAN_PATH, "cashflow.csv"))
analysis = pd.read_csv(os.path.join(CLEAN_PATH, "analysis.csv"))
pros = pd.read_csv(os.path.join(CLEAN_PATH, "prosandcons.csv"))
docs = pd.read_csv(os.path.join(CLEAN_PATH, "documents.csv"))

# -------------------------------
# 4. CLEAN COLUMN NAMES
# -------------------------------
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'[^a-z0-9]+', '_', regex=True)
    )
    return df

companies = clean_columns(companies)
balancesheet = clean_columns(balancesheet)
profit = clean_columns(profit)
cashflow = clean_columns(cashflow)
analysis = clean_columns(analysis)
pros = clean_columns(pros)
docs = clean_columns(docs)

# -------------------------------
# 5. FIX COMPANIES TABLE
# -------------------------------
print("🔍 BEFORE RENAME:", companies.columns)

# Rename columns based on your data
companies = companies.rename(columns={
    'id': 'symbol',
    'company': 'company_name'
})

print("🔍 AFTER RENAME:", companies.columns)

# Select required columns safely
if 'symbol' in companies.columns and 'company_name' in companies.columns:
    companies = companies[['symbol', 'company_name']]
else:
    print("❌ ERROR: Required columns not found!")
    print("Available columns:", companies.columns)
    exit()

# -------------------------------
# 6. LOAD TO DATABASE
# -------------------------------
companies.to_sql('companies', engine, if_exists='replace', index=False)
balancesheet.to_sql('balancesheet', engine, if_exists='replace', index=False)
profit.to_sql('profit', engine, if_exists='replace', index=False)
cashflow.to_sql('cashflow', engine, if_exists='replace', index=False)
analysis.to_sql('analysis', engine, if_exists='replace', index=False)
pros.to_sql('prosandcons', engine, if_exists='replace', index=False)
docs.to_sql('documents', engine, if_exists='replace', index=False)

print("🎉 SUCCESS: Data loaded into PostgreSQL!")