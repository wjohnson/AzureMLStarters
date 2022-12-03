# imports
import os
from pathlib import Path
import mlflow
import argparse

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from distutils.dir_util import copy_tree

def init():
    global OUTPUT_PATH
    global TEST_DATA_PATH
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="The input data path")
    parser.add_argument("--many_models_output_folder", help="The output of the many trained models")
    parser.add_argument("--testing_data_output_path", help="Path to store test data from training")
    # The parallel task will send a lot of other args
    args, unknown = parser.parse_known_args()

    TEST_DATA_PATH = args.testing_data_output_path
    OUTPUT_PATH = args.many_models_output_folder
    print(f"OUTPUT_PATH: {OUTPUT_PATH}")
    print(f"TEST_DATA_PATH: {TEST_DATA_PATH}")
    print(f"Unknown Args: {unknown}")
    print("INIT EXECUTED")

def prep_data(df:pd.DataFrame, datetime_column:str, dependent:str) -> pd.DataFrame:
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    df_agg = pd.DataFrame(df.groupby(datetime_column)[dependent].sum())

    start_date = min(df_agg.index.values)
    end_date = max(df_agg.index.values)
    t = np.arange(start_date, end_date, np.timedelta64(1, 'D'))

    remaining_days = np.setdiff1d(t, df_agg.index.values)
    remainder_df = pd.DataFrame(remaining_days)
    remainder_df[dependent] = 0
    remainder_df.columns = [datetime_column, dependent]
    remainder_df = remainder_df.set_index(datetime_column)

    df_dense = pd.concat([df_agg, remainder_df])
    df_dense = df_dense.sort_index()
    return df_dense

def train_model(df:pd.DataFrame, output_path:str, batch_name:str):
    mlflow.autolog()

    X = df.drop(["Quantity"], axis=1)
    y = df["Quantity"]
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    
    model = LinearRegression()
    pipe = Pipeline([('scaler', StandardScaler()), ('model', model)])
    pipe.fit(X_train, y_train)

    mlflow.sklearn.save_model(pipe, Path(output_path) / f"manymodelsv2/{batch_name}")

    return pipe, X_test, y_test

# Needs to return a pandas dataframe or list
def run(mini_batch):
    print(f'run method start: {__file__}, run({mini_batch} : {type(mini_batch)}')
    result_list = []
    for batch in mini_batch:
        batch_df = pd.read_csv(batch)
        distinct_values = batch_df["Country"].unique()
        print(f"Rows: {batch_df.shape[0]} Values: {distinct_values}")

        processed_df = prep_data(batch_df, "InvoiceDate", "Quantity")
        processed_df["lag1"] = processed_df["Quantity"].shift(-int(1))
        processed_df.dropna(inplace=True)

        model, X_test, y_test = train_model(processed_df, OUTPUT_PATH, distinct_values[0])

        print(f"X_test is {type(X_test)} and has {X_test.shape[0]} rows")
        # Adding in the batch name for later filtering
        group_name = distinct_values.tolist()[0]
        X_test["Country"] = group_name
        result_list.append(X_test[["Country"] + [x for x in X_test.columns if x != 'Country']])

    # If you're not writing a dataframe, you need to write the data
    # exactly as it should appear in the file. For example, you can't return a list of lists
    # you should return ','.join(my_list) to create a csv
    # Returning a dataframe makes it appear to be space delimited
    return pd.concat(result_list)
