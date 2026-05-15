import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Pinky1509@",
    host="localhost",
    port=5432,
    database="nifty_warehouse"
)

engine = create_engine(url)

print("✅ Connected to PostgreSQL")

# ---------------------------------
# CLEAN FUNCTION
# ---------------------------------

def clean_columns(df):

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace('%', 'pct')
        .str.replace(' ', '_')
        .str.replace(r'[^a-z0-9_]', '', regex=True)
    )

    return df

# ---------------------------------
# LOAD TABLES
# ---------------------------------

companies = pd.read_sql("SELECT * FROM companies", engine)

profit = pd.read_sql("SELECT * FROM profit", engine)
profit.columns = profit.iloc[0]
profit = profit[1:]

balancesheet = pd.read_sql("SELECT * FROM balancesheet", engine)
balancesheet.columns = balancesheet.iloc[0]
balancesheet = balancesheet[1:]

cashflow = pd.read_sql("SELECT * FROM cashflow", engine)
cashflow.columns = cashflow.iloc[0]
cashflow = cashflow[1:]

analysis = pd.read_sql("SELECT * FROM analysis", engine)
analysis.columns = analysis.iloc[0]
analysis = analysis[1:]

documents = pd.read_sql("SELECT * FROM documents", engine)
documents.columns = documents.iloc[0]
documents = documents[1:]

print("✅ Raw tables loaded")

# ---------------------------------
# CLEAN COLUMNS
# ---------------------------------

companies = clean_columns(companies)
profit = clean_columns(profit)
balancesheet = clean_columns(balancesheet)
cashflow = clean_columns(cashflow)
analysis = clean_columns(analysis)
documents = clean_columns(documents)

print("✅ Columns cleaned")

# ---------------------------------
# DIM COMPANY
# ---------------------------------

dim_company = companies[['symbol', 'company_name']]

dim_company = dim_company.drop_duplicates()

dim_company.to_sql(
    'dim_company',
    engine,
    if_exists='append',
    index=False
)

print("✅ dim_company loaded")

# ---------------------------------
# DIM YEAR
# ---------------------------------

year_rows = []

years = set()

for df in [profit, balancesheet, cashflow]:

    for col in df.columns:

        col = str(col)

        if (
            'mar' in col.lower()
            or 'dec' in col.lower()
            or 'jun' in col.lower()
            or 'sep' in col.lower()
            or 'ttm' in col.lower()
        ):
            years.add(col)

sort_order = 1

for y in sorted(years):

    fiscal_year = None

    if 'ttm' in y.lower():
        fiscal_year = 9999

    else:
        nums = ''.join(filter(str.isdigit, y))

        if nums:
            fiscal_year = int(nums[-4:])

    year_rows.append({
        'year_label': y,
        'fiscal_year': fiscal_year,
        'quarter': 'Q4',
        'is_ttm': 'ttm' in y.lower(),
        'is_half_year': False,
        'sort_order': sort_order
    })

    sort_order += 1

dim_year = pd.DataFrame(year_rows)

dim_year.to_sql(
    'dim_year',
    engine,
    if_exists='append',
    index=False
)

print("✅ dim_year loaded")

# ---------------------------------
# FACT TABLES
# ---------------------------------

profit.to_sql(
    'fact_profit_loss',
    engine,
    if_exists='replace',
    index=False
)

print("✅ fact_profit_loss loaded")

balancesheet.to_sql(
    'fact_balance_sheet',
    engine,
    if_exists='replace',
    index=False
)

print("✅ fact_balance_sheet loaded")

cashflow.to_sql(
    'fact_cash_flow',
    engine,
    if_exists='replace',
    index=False
)

print("✅ fact_cash_flow loaded")

analysis.to_sql(
    'fact_analysis',
    engine,
    if_exists='replace',
    index=False
)

print("✅ fact_analysis loaded")

documents.to_sql(
    'fact_documents',
    engine,
    if_exists='replace',
    index=False
)

print("✅ fact_documents loaded")

print("\n🎉 STAR SCHEMA BUILD COMPLETE!")