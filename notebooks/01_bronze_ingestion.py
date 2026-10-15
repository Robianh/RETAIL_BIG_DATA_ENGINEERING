
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"
BRONZE_DIR = PROJECT_DIR / "data" / "bronze"
OUTPUT_FILE = BRONZE_DIR / "retail_bronze.parquet"

print("RETAIL BIG DATA ENGINEERING")
print("BRONZE INGESTION")
print("-" * 45)

# Validate the source
if not SOURCE_FILE.exists():
    raise FileNotFoundError(
        f"Source dataset not found: {SOURCE_FILE}"
    )

BRONZE_DIR.mkdir(parents=True, exist_ok=True)

# Read source data without cleaning or filtering

# Read source data while preserving identifier columns as text
df = pd.read_excel(
    SOURCE_FILE,
    engine="openpyxl",
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "Description": "string",
        "CustomerID": "string",
        "Country": "string",
    }
)


source_record_count = len(df)

# Add lineage metadata
# Excel row 1 contains the column headers.
df["source_file"] = SOURCE_FILE.name
df["source_excel_row"] = range(2, source_record_count + 2)

# One UTC timestamp identifies this ingestion run.
df["ingestion_timestamp_utc"] = datetime.now(
    timezone.utc
).isoformat()

# Preserve source columns and append metadata.
df.to_parquet(
    OUTPUT_FILE,
    engine="pyarrow",
    index=False
)

print(f"Source records: {source_record_count:,}")
print(f"Bronze records: {len(df):,}")
print(f"Output file: {OUTPUT_FILE}")
print(f"Output size: {OUTPUT_FILE.stat().st_size / (1024 * 1024):.2f} MB")

# Read back the saved file to verify it
bronze_df = pd.read_parquet(OUTPUT_FILE)

print(f"Records read back: {len(bronze_df):,}")
print(f"Columns saved: {len(bronze_df.columns)}")

if len(bronze_df) != source_record_count:
    raise ValueError("Bronze row-count validation failed!")

print("PASS: Bronze row-count validation")
print("Bronze ingestion completed.")
