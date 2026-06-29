import great_expectations as gx
import pandas as pd
from great_expectations.checkpoint import UpdateDataDocsAction
import yaml


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

with open("scenarios.yaml") as f:
    scenarios = yaml.safe_load(f)

    for s in scenarios:
        meta = {"test_id":s["test_id"],
                "kpi":s["kpi"],
                "dimension":s["dimension"],
                "priority":s["priority"]}
        for col in s["columns"]:
            if s["type"] == "not_null":
                exp = gx.expectations.ExpectColumnValuesToNotBeNull(column = col, meta=meta,mostly=s.get("mostly",1.0))
            elif s["type"] == "between":
                exp = gx.expectations.ExpectColumnValuesToBeBetween(column = col, meta = meta,min_value = s.get("min_value"),
                                                                    max_value =s.get("max_value"),
                                                                    strict_min = s.get("strict_min",False))
            elif s["type"] == "unique":
                exp = gx.expectations.ExpectColumnValuesToBeUnique(column= col, meta = meta)
            elif s["type"] == "in_set":
                exp = gx.expectations.ExpectColumnValuesToBeInSet(column = col, meta = meta, value_set = s["value_set"])
            else:
                raise ValueError(f"Unknown type: {s['type']} in {s['test_id']}")
            suite.add_expectation(exp)

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



