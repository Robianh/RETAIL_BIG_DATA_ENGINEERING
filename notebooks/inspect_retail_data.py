
from pathlib import Path
import pandas as pd

# Locate the project and raw dataset
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"

print("NOVA RETAIL - DATA SOURCE INSPECTION")
print("-" * 45)

# Check that the file exists
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

print(f"Dataset: {DATA_FILE.name}")
print(f"File size: {DATA_FILE.stat().st_size / (1024 * 1024):.2f} MB")

# Load the Excel data
df = pd.read_excel(DATA_FILE, engine="openpyxl")

# Inspect the dataset
print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head().to_string())

print("\nColumn data types:")
print(df.dtypes.to_string())

print("\nMissing values per column:")
print(df.isna().sum().to_string())

print("\nDate range:")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
print(f"Earliest invoice: {df['InvoiceDate'].min()}")
print(f"Latest invoice:   {df['InvoiceDate'].max()}")

print("\nInspection completed.")

# ------------------------------------------
# DATA QUALITY AND TRANSACTION PROFILING
# ------------------------------------------

print("\nDATA QUALITY PROFILE")
print("-" * 45)

# 1. Cancelled invoice lines
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print(f"Rows with cancellation invoice numbers: {cancelled.sum():,}")

# 2. Quantity checks
negative_qty = df["Quantity"] < 0
zero_qty = df["Quantity"] == 0

print(f"Rows with negative quantity: {negative_qty.sum():,}")
print(f"Rows with zero quantity: {zero_qty.sum():,}")

# 3. Price checks
zero_price = df["UnitPrice"] == 0
negative_price = df["UnitPrice"] < 0

print(f"Rows with zero unit price: {zero_price.sum():,}")
print(f"Rows with negative unit price: {negative_price.sum():,}")

# 4. Duplicate records
duplicate_count = df.duplicated().sum()
print(f"Exact duplicate rows: {duplicate_count:,}")

# 5. Business key counts
print(f"Unique invoices: {df['InvoiceNo'].nunique():,}")
print(f"Unique products: {df['StockCode'].nunique():,}")
print(f"Unique customers: {df['CustomerID'].nunique():,}")
print(f"Unique countries: {df['Country'].nunique():,}")

# 6. Preliminary transaction value analysis
df["LineValue"] = df["Quantity"] * df["UnitPrice"]

positive_value = df.loc[df["LineValue"] > 0, "LineValue"].sum()
negative_value = df.loc[df["LineValue"] < 0, "LineValue"].sum()
net_value = df["LineValue"].sum()

print("\nPRELIMINARY TRANSACTION VALUES")
print(f"Positive line values: {positive_value:,.2f}")
print(f"Negative line values: {negative_value:,.2f}")
print(f"Net line value:       {net_value:,.2f}")

print("\nProfiling completed.")
