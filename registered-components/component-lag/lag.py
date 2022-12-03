# Source https://github.com/Azure/azureml-examples/blob/sdk-preview/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train-src/train.py

# imports
import os
import mlflow
import argparse

import pandas as pd
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


# define functions
def main(args):
    df = pd.read_csv(Path(args.data) / "intermediate.csv")
    for lagidx in args.lags.split(","):
        df["lag"+lagidx] = df[args.dependent].shift(-int(lagidx))
        
    df.dropna(inplace=True)

    # Write it out
    df.to_csv(Path(args.test_data) / "intermediate.csv", index=False)

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data", type=str)
    
    parser.add_argument("--lags", type=str, default="1,2,7,14")
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