# Data Quality Automation — Online Retail

A data quality pipeline that profiles a retail dataset, derives a test strategy, and validates it with Great Expectations, producing an HTML quality report.

## Overview

The project profiles the data with pandas, turns the findings into a documented test strategy (scenarios + KPIs), implements those scenarios as a Great Expectations suite, and runs a checkpoint that generates a Data Docs report.

## Dataset

[Online Retail & E-Commerce Dataset](https://www.kaggle.com/datasets/ertugrulesol/online-retail-data) (Kaggle, synthetic) — 1,000 rows, 13 columns: customer, product, transaction, and review fields.

## Approach

1. **Profile** the data with pandas (shape, nulls, ranges, distinct values).
2. **Define a test strategy** — 7 scenarios across Completeness, Uniqueness, and Validity, plus 7 quality KPIs. See `data_quality_test_strategy.md`.
3. **Implement** the scenarios as a Great Expectations expectation suite (each expectation tagged with its test ID and KPI via `meta`).
4. **Run** a checkpoint → Data Docs HTML report.

## Key Findings

14 expectations evaluated, 11 passed, 3 failed (≈78.6%).

- **review_score — 20.1% null.** Fails the 90% completeness threshold. A real gap in the data.
- **gender — 10.3% null.** Fails the 90% threshold; likely an optional field, flagged for review.
- **product_id uniqueness — 67.5% duplicates.** I initially asserted uniqueness on `product_id`. The report surfaced 
  67.5% duplicates — which is *correct*: in transaction data, a product is sold many times, so its id repeats by design. The real lesson is about **grain**: uniqueness must be tested on the table's key (a transaction/order id), not on a product or customer id that naturally recurs. The assumption was corrected after reading the validation results.

## How to run

pip install -r requirements.txt
python main.py

The dataset CSV sits next to main.py. The report is generated at gx/uncommitted/data_docs/local_site/index.html and opens automatically.

Files:
main.py — profiling + Great Expectations pipeline
data_quality_test_strategy.md — test scenarios and KPIs
requirements.txt — dependencies