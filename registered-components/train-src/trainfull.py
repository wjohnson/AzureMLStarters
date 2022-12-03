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
from distutils.dir_util import copy_tree

# define functions
def main(args):
    # enable auto logging
    mlflow.autolog()

    # setup parameters
    params = {
        "fit_intercept": args.fit_intercept
    }

    # read in data
    df = pd.read_csv(args.data)

    df['InvoiceDateOnly'] = pd.to_datetime(df["InvoiceDateOnly"])
    df_agg = pd.DataFrame(df.groupby("InvoiceDateOnly")['Quantity'].sum())

    start_date = min(df_agg.index.values)
    end_date = max(df_agg.index.values)
    t = np.arange(start_date, end_date, np.timedelta64(1, 'D'))

    remaining_days = np.setdiff1d(t, df_agg.index.values)
    remainder_df = pd.DataFrame(remaining_days)
    remainder_df["Quantity"] = 0
    remainder_df.columns = ["InvoiceDateOnly", "Quantity"]
    remainder_df = remainder_df.set_index("InvoiceDateOnly")

    df_dense = pd.concat([df_agg, remainder_df])
    df_dense = df_dense.sort_index()

    df_dense["lag1"] = df_dense["Quantity"].shift(-1)
    df_dense["lag2"] = df_dense["Quantity"].shift(-2)
    df_dense["lag7"] = df_dense["Quantity"].shift(-7)
    df_dense["lag14"] = df_dense["Quantity"].shift(-14)
    df_dense.dropna(inplace=True)

    X = df_dense.drop(["Quantity"], axis=1)
    y = df_dense["Quantity"]
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=args.random_state
        )
    
    model = LinearRegression()
    pipe = Pipeline([('scaler', StandardScaler()), ('model', model)])
    pipe.fit(X_train, y_train)

    mlflow.sklearn.save_model(pipe, "model")

    # copy subdirectory example
    from_directory = "model"
    to_directory = args.model_output

    copy_tree(from_directory, to_directory)

    X_test.to_csv(Path(args.test_data) / "X_test.csv", index=False)
    y_test.to_csv(Path(args.test_data) / "y_test.csv", index=False)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--data", type=str)
    
    parser.add_argument("--random_state", type=int, default=42)
    parser.add_argument("--model_output", type=str, help="Path of output model")
    parser.add_argument("--test_data", type=str, help="Path of output model")
    parser.add_argument("--fit_intercept", type=bool, default=True)

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