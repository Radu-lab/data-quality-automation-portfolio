# pyspark-cyber-dq

Data quality testing on PySpark transformations, using network-traffic /
cyber-attack data.

Same approach as the flight project — validating a PySpark pipeline with two
complementary kinds of testing:
- **Data quality checks on real data** — properties of the actual dataset
  (reconciliation, null checks, uniqueness).
- **Transformation logic unit tests** — verifying the aggregation functions
  produce the correct output on small, controlled data, using chispa.

## What it does

- `helpers.py` loads the data and exposes the transformations as reusable functions:
- `init_df` — loads the CSV into a Spark DataFrame
- `aggregate` — groups by protocol, summing failed logins and packet count
- `aggregate2` — groups by attack type and protocol, averaging duration and
  summing source/destination bytes

## Tests

- `test_pipeline.py` — data quality checks on the real data (null, uniqueness) using plain assertions.
- `test_transforms.py` — chispa unit tests on `aggregate` and `aggregate2`:
  small hand-built input, hand-written expected output, compared with
  `assert_df_equality`. Verifies the logic independent of the real data.

The two catch different problems: data checks guard the real data; chispa guards
the transformation logic.
Reconciliation was not needed due to simple aggregation of groupBy+sum - all rows into one group,
as no joins were used.

## Structure

    pyspark-cyber-dq/
    ├── helpers.py          # init_df, aggregate, aggregate2
    ├── main.py             # exploration script
    ├── conftest.py         # shared Spark fixture
    ├── test_pipeline.py    # data quality (asserts, real data)
    ├── test_transforms.py  # logic (chispa, toy data)
    └── <cyber CSV>

## Running

    pip install pyspark chispa pytest
    pytest

## Notes

- Network-traffic dataset from Kaggle.
- The CSV path in `helpers.py` is currently absolute — adjust it to point to the
  local CSV if running elsewhere.
- Self-directed upskilling project, not production code.