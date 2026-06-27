import great_expectations as gx
import pandas as pd
from great_expectations.checkpoint import UpdateDataDocsAction


df = pd.read_csv("synthetic_online_retail_data.csv")

#profiling data
print("Shape:",df.shape)
print("\nColumns\n",df.columns.tolist())
print("\nInfo:")
print(df.info())
print("\nMissing values:\n",df.isnull().sum())
print("\nSample data: ")
print(df.head())
print("\nBasic statistics: ")
print(df.describe())
print(df.describe().T[["min","max"]])
print(df["gender"].unique())
print(df["payment_method"].unique())

#
context = gx.get_context(mode="file")
data_source_name = "retail_data"
data_source = context.data_sources.add_or_update_pandas(name=data_source_name)

try:
    data_asset = data_source.get_asset("Retail Data")

except Exception:
     data_asset = data_source.add_dataframe_asset(name = "Retail Data")

#create batch definition
batch_definition_name = "retail_batch"
try:
    batch_definition = data_asset.get_batch_definition("batch_definition_name")

except Exception:
      
    batch_definition = data_asset.add_batch_definition_whole_dataframe(name = batch_definition_name)

batch_parameters = {"dataframe":df}

# Get the dataframe as a Batch
batch = batch_definition.get_batch(batch_parameters=batch_parameters)

#create suite for expectations
suite = gx.ExpectationSuite(name="retail_suite")
suite = context.suites.add_or_update(suite)

#define expectations
#Test-01
meta_01 = {"test_id": "Test-01",
           "kpi": "KPI-01",
           "dimension": "Completeness",
           "priority": "High"}
for col in ["customer_id","order_date","product_id","quantity","price"]:
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(meta = meta_01,column = col))

#Test-02
meta_02 = {"test_id": "Test-02",
           "kpi": "KPI-02",
           "dimension": "Completeness",
           "priority": "High"}
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(meta = meta_02,mostly = 0.90,
                                                                    column = "review_score"))
#Test-03
meta_03 = {"test_id": "Test-03",
           "kpi": "KPI-03",
           "dimension": "Completeness",
           "priority": "Medium"}
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(meta = meta_03,mostly=0.90,column = "gender"))

#Test-04
meta_04 = {"test_id": "Test-04",
           "kpi": "KPI-04",
           "dimension": "Uniqueness",
           "priority": "High"}
for col in ["customer_id","product_id"]:
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(meta = meta_04,column = col))

#Test-05
meta_05 = {"test_id": "Test-05",
           "kpi": "KPI-05",
           "dimension": "Validity",
           "priority": "High"}
for col in ["quantity","price"]:
        suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(meta = meta_05,min_value = 0,column = col))

#Test-06
meta_06 = {"test_id": "Test-06",
           "kpi": "KPI-06",
           "dimension": "Validity",
           "priority": "High"}
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(meta = meta_06,min_value = 1,
                                                                    max_value= 5,column = "review_score"))

#Test-07
meta_07 = {"test_id": "Test-07",
           "kpi": "KPI-07",
           "dimension": "Validity",
           "priority": "High"}
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(meta = meta_07,column="gender", 
                                                                  value_set=["F", "M"]))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(meta = meta_07,
                                                                  column="payment_method",
                                                                value_set=['Credit Card', 'Bank Transfer', 'Cash on Delivery']))
definition_name = "validation"
validation_definition = gx.ValidationDefinition(data = batch_definition,
                                                suite = suite,
                                                name = definition_name)
validation_definition = context.validation_definitions.add_or_update(validation_definition)

#checkpoint
action_list = [
    # This Action updates the Data Docs static website with the Validation
    #   Results after the Checkpoint is run.
    UpdateDataDocsAction(
        name="update_all_data_docs",
    ),
]
checkpoint_name = "my_checkpoint"
checkpoint = gx.Checkpoint(
    name=checkpoint_name,
    validation_definitions=[validation_definition],
    actions=action_list,
    result_format={"result_format": "COMPLETE"},
)
context.checkpoints.add_or_update(checkpoint)
#run the checkpoint
validation_results = checkpoint.run(batch_parameters=batch_parameters)
context.open_data_docs()



