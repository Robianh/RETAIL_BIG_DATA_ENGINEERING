
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
BRONZE_FILE = PROJECT_DIR / "data" / "bronze" / "retail_bronze.parquet"
SILVER_DIR = PROJECT_DIR / "data" / "silver"
SILVER_FILE = SILVER_DIR / "retail_silver.parquet"

print("RETAIL BIG DATA ENGINEERING")
print("SILVER TRANSFORMATION")
print("-" * 45)

# Read Bronze data
df = pd.read_parquet(BRONZE_FILE)
bronze_count = len(df)

# Define source columns before adding quality flags
source_columns = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]

# Standardize data types
df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["CustomerID"] = df["CustomerID"].astype("string").str.strip()
df["Description"] = df["Description"].astype("string").str.strip()
df["Country"] = df["Country"].astype("string").str.strip()

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Quality flags: preserve the records
df["is_cancelled_invoice"] = (
    df["InvoiceNo"].str.startswith("C", na=False)
)

df["has_negative_quantity"] = df["Quantity"] < 0
df["has_missing_customer_id"] = (
    df["CustomerID"].isna() | df["CustomerID"].eq("")
)
df["has_missing_description"] = (
    df["Description"].isna() | df["Description"].eq("")
)
df["has_zero_unit_price"] = df["UnitPrice"] == 0
df["has_negative_unit_price"] = df["UnitPrice"] < 0
df["has_invalid_quantity"] = df["Quantity"].isna()
df["has_invalid_unit_price"] = df["UnitPrice"].isna()
df["has_invalid_invoice_date"] = df["InvoiceDate"].isna()

# Flag every member of an exact duplicate group.
# Ignore ingestion metadata when comparing source records.
df["is_exact_duplicate"] = df.duplicated(
    subset=source_columns,
    keep=False
)

# Calculate the preliminary transaction line value
df["LineValue"] = df["Quantity"] * df["UnitPrice"]

# Save Silver data
SILVER_DIR.mkdir(parents=True, exist_ok=True)
df.to_parquet(SILVER_FILE, index=False)

# Read back and validate
silver_check = pd.read_parquet(SILVER_FILE)

print(f"Bronze records: {bronze_count:,}")
print(f"Silver records: {len(silver_check):,}")
print(f"Output file: {SILVER_FILE}")

print("\nQUALITY FLAG COUNTS")
for column in [
    "is_cancelled_invoice",
    "has_negative_quantity",
    "has_missing_customer_id",
    "has_missing_description",
    "has_zero_unit_price",
    "has_negative_unit_price",
    "has_invalid_quantity",
    "has_invalid_unit_price",
    "has_invalid_invoice_date",
    "is_exact_duplicate",
]:
    print(f"{column}: {int(silver_check[column].sum()):,}")

if len(silver_check) != bronze_count:
    raise ValueError("Silver row-count validation failed!")

print("\nPASS: Silver row-count validation")
print("Silver transformation completed.")
