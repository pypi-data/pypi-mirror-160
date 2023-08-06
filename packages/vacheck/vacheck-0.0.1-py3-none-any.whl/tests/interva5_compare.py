from vacheck.datacheck5 import datacheck5
import pandas as pd
from numpy import nan
import os

working_dir = os.getcwd()
data_path = os.path.join(working_dir, "iv5_sample.csv")
# data_path = os.path.join(working_dir, "tests", "iv5_sample.csv")
iv5_sample = pd.read_csv(data_path)
iv5_sample.replace(['Y', 'N', '-'], [1, 0, nan], inplace=True)
id_col = iv5_sample.pop("iv5_id")
iv5_sample.insert(0, "ID", id_col)
all_results = {}
all_first_pass = ["First Pass"]
all_second_pass = ["Second Pass"]
for i in range(iv5_sample.shape[0]):
    i_id = iv5_sample.iloc[i]["ID"]
    results = datacheck5(iv5_sample.iloc[i], i_id)
    all_results[i_id] = results["output"]
    all_first_pass.extend(results["first_pass"])
    all_second_pass.extend(results["second_pass"])

# df_results = pd.DataFrame(all_results)
# df_results.to_csv("results_iv5_sample.csv")

log_results_path = os.path.join(working_dir,
                                "iv5_sample_vacheck_log.txt")
# log_results_path = os.path.join(working_dir, "tests",
#                                 "example_input_vacheck_log.txt")
all_first_pass.extend(all_second_pass)
with open(log_results_path, "w") as text_file:
    for item in all_first_pass:
        text_file.write(f"{item}\n")


data_path = os.path.join(working_dir, "example_input.csv")
# data_path = os.path.join(working_dir, "tests", "example_input.csv")
example_input = pd.read_csv(data_path)

all_results = {}
all_first_pass = ["First Pass"]
all_second_pass = ["Second Pass"]
for i in range(example_input.shape[0]):
    i_id = example_input.iloc[i]["ID"]
    results = datacheck5(example_input.iloc[i], i_id)
    all_results[i_id] = results["output"]
    all_first_pass.extend(results["first_pass"])
    all_second_pass.extend(results["second_pass"])

# df_results = pd.DataFrame(all_results)
# df_results.to_csv("results_example_input.csv")

log_results_path = os.path.join(working_dir,
                                "example_input_vacheck_log.txt")
# log_results_path = os.path.join(working_dir, "tests",
#                                 "example_input_vacheck_log.txt")
all_first_pass.extend(all_second_pass)
with open(log_results_path, "w") as text_file:
    for item in all_first_pass:
        text_file.write(f"{item}\n")
