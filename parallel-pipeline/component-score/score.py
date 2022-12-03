# imports
import os
from pathlib import Path
import mlflow
import argparse

import pandas as pd

def list_if_dir(path:str):
    print(f"Working with {path}")
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(args.testing_data_path):
            print(dirpath, dirnames, filenames)
    else:
        print(f"{path} is not a directory")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testing_data_path", help="The input data path")
    parser.add_argument("--models", help="The path to the models")
    parser.add_argument("--prediction", help="The output data path")
    # The parallel task will send a lot of other args
    args, unknown = parser.parse_known_args()

    list_if_dir(args.testing_data_path)
    list_if_dir(args.models)
    list_if_dir(args.prediction)

    # Load models
    MODELS = {}
    for dirpath, dirnames, filenames in os.walk(args.models):
        if "model.pkl" in filenames:
            model_name = Path(dirpath).stem
            print(f"Loading model for {model_name}")
            _model = mlflow.sklearn.load_model(dirpath)
            MODELS[model_name] = _model

    # Scoring
    df = pd.read_csv(args.testing_data_path, header=None, sep=" ")

    predictions = []
    # Hard coded the first column to be the grouping column
    # This may need to be changed
    known_groups = df[0].unique()
    for group in known_groups:
        if group not in MODELS:
            print(f"Failed to load model for {group}")
        # TODO: Would need more data processing
        _model = MODELS[group]
        _local_df = df.loc[ df[0] == group, 1: ]
        # Predict on all columns (except first which contains the grouping) for all rows
        # that are in the group
        _local_df["prediction"] = _model.predict(_local_df)
        predictions.append(_local_df)
    
    all_predictions = pd.concat(predictions)
    
    # Writing out
    all_predictions.to_csv(Path(args.prediction) / "predictions.csv")
