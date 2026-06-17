# pyspark-flight-dq

Data quality testing on a PySpark transformation, using flight data.

This project demonstrates two complementary kinds of testing for a PySpark
data pipeline:

- **Data quality checks on real data** — validating properties of the actual
  dataset (reconciliation between raw and aggregated totals).
- **Transformation logic unit tests** — verifying the aggregation function
  produces the correct output on small, controlled data, using the chispa library.

## What it does

`helpers.py` loads the flight data and exposes the transformation as a reusable
function:
- `init_df` — loads the CSV into a Spark DataFrame
- `aggregate` — groups by entity, model and month, summing distance flown

The same `aggregate` function is used by the reconciliation test and tested in
isolation by chispa.

## Tests

- `test_pipeline.py` → `test_reconciliation`: runs on the real data and asserts
  that the total distance is preserved after aggregation (nothing lost or duplicated).
- `test_transforms.py` → `test_aggregate`: feeds `aggregate` a small hand-built
  DataFrame and uses `assert_df_equality` (chispa) to check the output matches the
  expected result exactly. Verifies the transformation logic, independent of real data.

The two catch different problems: reconciliation guards the totals on real data;
the chispa test guards the aggregation logic.

## Structure

    pyspark-flight-dq/
    ├── helpers.py          # init_df, aggregate
    ├── main.py             # exploration script
    ├── conftest.py         # shared Spark fixture
    ├── test_pipeline.py    # data quality (asserts, real data)
    ├── test_transforms.py  # logic (chispa, toy data)
    └── flight_data2026.csv

## Running

    pip install pyspark chispa pytest
    pytest

## Notes

- Flight data from Kaggle.
- The CSV path in `helpers.py` / `main.py` is currently absolute — adjust it to
  point to `flight_data2026.csv` in this folder if running elsewhere.
- Self-directed upskilling project, not production code.
