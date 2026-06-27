# Data Quality Test Strategy

**Project:** QA Data Quality Portfolio  
**Dataset:** Online Retail / Sales Transactions  
**Rows:** 1,000
**Columns:** 13  
**Date:** June 25, 2026

## 1. Dataset Overview
This dataset contains sales transactions with customer, product, and review information. It has notable data quality issues, particularly missing values in `review_score` and `gender`, and potential uniqueness problems with `product_id`.
The findings were done profiling the data with pandas.

## 2. Quality KPIs

| KPI ID | KPI Name                  | Definition                                       | Target Threshold | Priority |
| ------ | ------------------------- | ------------------------------------------------ | ---------------- | -------- |
| KPI-01 | Overall Completeness      | Percentage of non-null values across columns     | >=95%            | High     |
| KPI-02 | Review Score Completeness | % of records with `review_score` filled          | >90%             | High     |
| KPI-03 | Gender Completeness       | % of records with `gender` filled                | >90%             | Medium   |
| KPI-04 | Uniqueness Rate           | % of unique `customer_id` and `product_id`       | 100%             | High     |
| KPI-05 | Validity Rate             | % of records with `price` and `quantity` >0      | >=95%            | High     |
| KPI-06 | Review Score Validity     | % of records with `review_score` between 1 and 5 | >99%             | High     |
| KPI-07 | Categorical Validity      | % of records with valid values in categorical fields | >=99%        | High     |

## 3. Test Scenarios

**Test-01**  
**Dimension:** Completeness  
**KPI ID:** `KPI-01`
**Objective:** Ensure critical fields have acceptable completeness.  
**Columns:** `customer_id`, `order_date`, `product_id`, `quantity`, `price`  
**Expected Result:** 0 missing values (or ≤ 1%).  
**GE Expectation:** `ExpectColumnValuesToNotBeNull()`
**Priority:** High

**Test-02**
**Dimension:** Completeness
**KPI ID:** `KPI-02`
**Objective:** Measure review score completeness.
**Columns:** `review_score`
**Expected Result:** Missing values ≤ 10% (improve from current 20.1%).
**GE Expectation:** `ExpectColumnValuesToNotBeNull(mostly = 0.90)`
**Priority:** High

**Test-03**
**Dimension:** Completeness
**KPI ID:** `KPI-03`
**Objective:** Ensure gender information is mostly complete
**Columns:** `gender`
**Expected Result:** Missing values ≤ 10%
**GE Expectation:** `ExpectColumnValuesToNotBeNull(mostly=0.90)`
**Priority:** Medium

**Test-04**
**Dimension:** Uniqueness
**KPI ID:** `KPI-04`
**Objective:** Verify that customer and product identifiers are unique.
**Columns:** `customer_id`,`product_id`
**Expected Result:** No duplicate values in identifier columns.
**GE Expectation:** `ExpectColumnValuesToBeUnique()`
**Priority:** High

**Test-05**  
**Dimension:** Validity
**KPI ID:** `KPI-05`  
**Objective:** Validate that numerical fields contain logical positive values.  
**Columns:** `quantity`, `price`  
**Expected Result:** `quantity` > 0 and `price` > 0.  
**GE Expectation:** `ExpectColumnValuesToBeBetween(min_value=0)`  
**Priority:** High

**Test-06**  
**Dimension:** Validity
**KPI ID:** `KPI-06`  
**Objective:** Validate review scores fall within acceptable range.  
**Columns:** `review_score`  
**Expected Result:** Values between 1 and 5.  
**GE Expectation:** `ExpectColumnValuesToBeBetween(min_value=1, max_value=5)`  
**Priority:** High

**Test-07**  
**Dimension:** Validity  
**KPI ID:** `KPI-07`
**Objective:** Validate categorical fields contain only expected values.  
**Columns:** `payment_method`, `gender`  
**Expected Result:** Only valid categories are present.  
**GE Expectation:** `ExpectColumnValuesToBeInSet()`  
**Priority:** Medium
