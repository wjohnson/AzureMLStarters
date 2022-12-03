# Source https://github.com/Azure/azureml-examples/blob/sdk-preview/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train-src/train.py

# imports
import argparse

import pandas as pd
from pathlib import Path
import pandas as pd


# define functions
def main(args):
    # We know that the file is an excel file
    df = pd.read_excel(args.data, sheet_name="Year 2009-2010")
    
    df["InvoiceDateOnly"] = df["InvoiceDate"].dt.date
    training_data = df.groupby(["InvoiceDateOnly", "StockCode"])["Quantity"].sum().reset_index()

    # Write it out
    training_data.to_csv(Path(args.prepared_data), index=False)

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data", type=str)
    parser.add_argument("--prepared_data", type=str, default="Path of output data")

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # parse args
    args = parse_args()

    # run main function
    main(args)