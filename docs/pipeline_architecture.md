# Retail Data Engineering Pipeline Architecture

## 1. Purpose

This document describes the architecture of the Retail Big Data Engineering project. The pipeline processes online retail transactions through Bronze, Silver, and Gold data layers using Python, SQL, Apache Spark, Databricks, and Delta Lake.

## 2. Data Source

The project uses the Online Retail dataset from the UCI Machine Learning Repository.

Source: https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains 541,909 transaction-line records covering December 2010 through December 2011.

## 3. Pipeline Layers

### Bronze Layer

**Table:** `workspace.datadata.bronze_retail_transactions`

The Bronze layer stores ingested source records with additional ingestion metadata. It preserves the source data for traceability and further processing.

### Silver Layer

**Table:** `workspace.datadata.silver_retail_transactions`

The Silver layer standardizes text fields, calculates transaction-line values, and adds data-quality flags for issues such as missing customer IDs, missing descriptions, cancellation invoices, negative quantities, and unusual prices.

Records are retained so that data-quality issues can be investigated.

### Gold Layer

The Gold layer contains aggregated data for reporting and analysis.

- `workspace.datadata.gold_monthly_sales`: monthly sales summaries.
- `workspace.datadata.gold_country_sales`: country-level sales summaries.

These tables support analysis of sales trends and geographic performance.

## 4. Preliminary Sales Rules

The initial Gold analysis excludes cancellation invoices, non-positive quantities, and non-positive unit prices.

The resulting sales values are preliminary gross sales estimates. They should not be interpreted as profit or confirmed net revenue without further accounting and business-rule validation.

## 5. Technology Stack

- Python and PySpark
- SQL
- Apache Spark
- Databricks
- Delta Lake
- Parquet

## 6. Future Improvements

- Add automated data-quality tests.
- Implement incremental data ingestion.
- Schedule and monitor pipeline execution.
- Develop a sales dashboard.
- Document deployment and reproducibility steps.