# Source https://github.com/Azure/azureml-examples/blob/sdk-preview/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train-src/train.py

# imports
import os
import mlflow
import argparse

import pandas as pd
from pathlib import Path


import pandas as pd
import numpy as np


# define functions
def main(args):
    df = pd.read_csv(args.data)
    

    df[args.datetime_column] = pd.to_datetime(df[args.datetime_column])
    df_agg = pd.DataFrame(df.groupby(args.datetime_column)[args.dependent].sum())

    start_date = min(df_agg.index.values)
    end_date = max(df_agg.index.values)
    t = np.arange(start_date, end_date, np.timedelta64(1, 'D'))

    remaining_days = np.setdiff1d(t, df_agg.index.values)
    remainder_df = pd.DataFrame(remaining_days)
    remainder_df[args.dependent] = 0
    remainder_df.columns = [args.datetime_column, args.dependent]
    remainder_df = remainder_df.set_index(args.datetime_column)

    df_dense = pd.concat([df_agg, remainder_df])
    df_dense = df_dense.sort_index()

    # Write it out
    df_dense.to_csv(Path(args.test_data) / "intermediate.csv", index=False)

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data", type=str)
    
    parser.add_argument("--datetime_column", type=str, default="date")
    parser.add_argument("--dependent", type=str, help="Name of dependent variable")
    parser.add_argument("--test_data", type=str, help="Path of output data")

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