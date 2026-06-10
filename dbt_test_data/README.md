Data Quality Pipelines (dbt + DuckDB)
A dbt project that cleans, transforms, and tests data across three datasets. The focus is data quality: understand what the data actually is before transforming it, and turn that understanding into automated tests.

1. Flight data

The data

Daily flight-efficiency records. One row per entity (a country or airspace block), per trajectory model, per day, with three distance columns: flown, direct, and achieved (km).
The type_model column has three values - FTFM, CPF, and SFR. These are three different trajectory models for the same flights, not three separate things. Adding them together would count the same flights three times, so the pipeline keeps type_model as a grouping column instead of summing across it.

How it's built

raw CSV  ->  staging (cleaned, daily)  ->  aggregation (monthly totals)

stg_flight_data2026 cleans the raw data and keeps the daily detail.
monthly_results sums the daily distances into monthly totals, per entity and per trajectory model (GROUP BY entity_name, type_model, month_num).

Cleaning and aggregation are kept as separate steps, so the daily detail stays available and testable.

The grain investigation

I added a uniqueness test on what I assumed identified one row: entity_name + type_model + month_num.
It failed - 648 violations.
Instead of deleting the test to make it pass, I checked the data in DBeaver:

Grouped by the assumed key and counted - every combination appeared exactly 30 times.
April has 30 days. So the data is daily, not monthly.
Confirmed by looking at entry_date - 30 different dates per combination, one per day.

My assumption was wrong. A row is actually identified by entity_name + type_model + entry_date (daily); month_num was just taken from the date. I fixed the test to match the real data - it now passes and documents how the data is actually structured.

Tests

*not_null on the three distance columns.
*Uniqueness on the daily key (entity_name + type_model + entry_date).
*Uniqueness on the monthly key after aggregation — confirms no duplicate groups.
*A reconciliation test: the total of the daily distances must equal the total of the monthly results. If they differ, rows were dropped or double-counted during aggregation. (Exact match on the whole-number column, a small tolerance on the decimal ones to avoid rounding false alarms.


2. Orders
A first pipeline on a messy orders CSV. Staging cleans the data (lower-casing inconsistent status values, removing duplicate rows); a second step aggregates revenue per customer. A uniqueness test on order_id caught a duplicated order, fixed in staging with DISTINCT — the same idea as above, on a simpler case.

3. Consumer orders — sources and freshness
A retail-orders dataset used to try out two dbt features: declaring a table that already exists in the database as a source(), and adding a freshness check on its date column to flag data that has gone stale.

Tech

dbt-core, dbt-duckdb, dbt_utils. DuckDB as the local database. DBeaver for looking at the data directly.
Run
pip install dbt-core dbt-duckdb
dbt deps
dbt seed
dbt run
dbt test