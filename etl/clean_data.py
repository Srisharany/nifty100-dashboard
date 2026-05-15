import pandas as pd
import os

# Paths
RAW_PATH = r'D:\BLUESTOCK\Task2\nifty_project\data\raw'
CLEAN_PATH = r'D:\BLUESTOCK\Task2\nifty_project\data\clean'

# Create clean folder if not exists
os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------------
# 1. Load files
# -------------------------------
companies = pd.read_excel(os.path.join(RAW_PATH, "companies.xlsx"))
balancesheet = pd.read_excel(os.path.join(RAW_PATH, "balancesheet.xlsx"))
profit = pd.read_excel(os.path.join(RAW_PATH, "profitandloss.xlsx"))
cashflow = pd.read_excel(os.path.join(RAW_PATH, "cashflow.xlsx"))
analysis = pd.read_excel(os.path.join(RAW_PATH, "analysis.xlsx"))
pros = pd.read_excel(os.path.join(RAW_PATH, "prosandcons.xlsx"))
docs = pd.read_excel(os.path.join(RAW_PATH, "documents.xlsx"))

# -------------------------------
# 2. Clean common issues
# -------------------------------
def clean_df(df):
    df = df.replace(['NULL', 'Null'], pd.NA)
    df.columns = df.columns.str.strip()
    return df

companies = clean_df(companies)
balancesheet = clean_df(balancesheet)
profit = clean_df(profit)
cashflow = clean_df(cashflow)
analysis = clean_df(analysis)
pros = clean_df(pros)
docs = clean_df(docs)

# -------------------------------
# 3. Standardize Year
# -------------------------------
def fix_year(year):
    if pd.isna(year):
        return None
    
    year = str(year)

    if "Mar-" in year:
        return "Mar 20" + year.split("-")[1]
    elif "TTM" in year:
        return "TTM"
    else:
        return year

for df in [balancesheet, profit, cashflow]:
    if "year" in df.columns:
        df["year"] = df["year"].apply(fix_year)

# -------------------------------
# 4. Compute important metrics
# -------------------------------

# Profit metrics
if "net_profit" in profit.columns and "sales" in profit.columns:
    profit["net_profit_margin"] = (profit["net_profit"] / profit["sales"]) * 100

# Balance sheet metrics
if "borrowings" in balancesheet.columns and "reserves" in balancesheet.columns:
    balancesheet["debt_to_equity"] = balancesheet["borrowings"] / balancesheet["reserves"]

# Cashflow metrics
if "operating_activity" in cashflow.columns and "investing_activity" in cashflow.columns:
    cashflow["free_cash_flow"] = cashflow["operating_activity"] + cashflow["investing_activity"]

# -------------------------------
# 5. Save cleaned data
# -------------------------------
companies.to_csv(os.path.join(CLEAN_PATH, "companies.csv"), index=False)
balancesheet.to_csv(os.path.join(CLEAN_PATH, "balancesheet.csv"), index=False)
profit.to_csv(os.path.join(CLEAN_PATH, "profit.csv"), index=False)
cashflow.to_csv(os.path.join(CLEAN_PATH, "cashflow.csv"), index=False)
analysis.to_csv(os.path.join(CLEAN_PATH, "analysis.csv"), index=False)
pros.to_csv(os.path.join(CLEAN_PATH, "prosandcons.csv"), index=False)
docs.to_csv(os.path.join(CLEAN_PATH, "documents.csv"), index=False)

print("✅ Data cleaned and saved successfully!")