# Retail Big Data Engineering Project

## Overview

This project implements an end-to-end retail data engineering pipeline using Python, SQL, Apache Spark, Databricks, and Delta Lake. It processes online retail transaction data through Bronze, Silver, and Gold layers to support data quality checks and business analytics.

## Project Objectives

- Ingest and validate retail transaction data.
- Build structured Bronze, Silver, and Gold data layers.
- Apply data standardization and data-quality checks.
- Analyze monthly sales trends and country-level performance.
- Prepare reliable analytical tables for reporting and dashboards.

## Technology Stack

- **Python** — data processing and pipeline development
- **SQL** — data validation and analytical queries
- **Apache Spark / PySpark** — distributed data processing
- **Databricks** — data engineering workspace
- **Delta Lake** — managed analytical tables
- **Parquet** — columnar data storage

## Data Source

The project uses the Online Retail dataset from the UCI Machine Learning Repository.

Dataset: https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains 541,909 transaction-line records from an online retailer, covering December 2010 through December 2011.

## Pipeline Architecture

```text
Source Excel Dataset
        |
        v
Bronze Layer
Raw ingested records
        |
        v
Silver Layer
Standardized data and quality flags
        |
        v
Gold Layer
Monthly and country-level sales summaries
```

## Data Layers

### Bronze

Table: `workspace.datadata.bronze_retail_transactions`

- 541,909 records
- 11 columns
- Stores ingested source data with ingestion metadata.

### Silver

Table: `workspace.datadata.silver_retail_transactions`

- 541,909 records
- 18 columns
- Standardizes text fields.
- Flags cancellation invoices, negative quantities, missing customer IDs, missing descriptions, and unusual prices.
- Calculates transaction-line values.
- Preserves records for investigation rather than deleting them indiscriminately.

### Gold

**Monthly sales table**

`workspace.datadata.gold_monthly_sales`

- 13 monthly summary rows
- Reports sales lines, invoice counts, and gross sales value.

**Country sales table**

`workspace.datadata.gold_country_sales`

- 38 country-category summary rows
- Reports sales lines, invoice counts, and gross sales value.

## Preliminary Findings

- Total source records: 541,909.
- Distinct invoice numbers in the source data: 25,900.
- Distinct product stock codes: 4,070.
- Distinct customer IDs: 4,372.
- Distinct country values: 38.
- November 2011 had the highest monthly gross sales value in the filtered analysis: approximately £1,509,496.33.
- The United Kingdom had the highest country-level gross sales value: approximately £9,025,222.08.

## Data Quality

The pipeline identifies missing customer IDs and descriptions, cancellation invoice numbers, negative quantities, and zero or negative unit prices.

The preliminary sales analysis excludes cancellation invoices, non-positive quantities, and non-positive unit prices. Its gross sales values are not profit or confirmed net revenue. Returns, accounting adjustments, costs, and other business rules require further analysis.

## Repository Structure

```text
RETAIL_BIG_DATA_ENGINEERING/
├── data/
│   ├── raw/
│   ├── bronze/
│   └── silver/
├── notebooks/
├── sql/
├── docs/
├── .gitignore
└── README.md
```

Generated data files are excluded from Git tracking. The repository is intended to hold source code, SQL scripts, documentation, and project configuration.

## Future Improvements

- Automate and schedule the pipeline.
- Add repeatable data-quality tests.
- Create reusable SQL analytics.
- Build a sales dashboard.
- Document setup and execution instructions.
- Add incremental ingestion and monitoring.

## Project Status

The initial Bronze-to-Silver-to-Gold pipeline has been implemented in Databricks, and the saved tables have been checked using SQL. Automation, comprehensive testing, and dashboard development remain future improvements.
