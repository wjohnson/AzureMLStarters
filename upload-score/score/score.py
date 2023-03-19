# imports
import os
from pathlib import Path
import joblib
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
    parser.add_argument("--model", help="The path to the models")
    parser.add_argument("--prediction", help="The output data path")
    # The task may send a lot of other args
    args, unknown = parser.parse_known_args()

    list_if_dir(args.testing_data_path)
    list_if_dir(args.model)
    list_if_dir(args.prediction)

    # Load models
    model = None
    if not os.path.exists(args.model):
        raise Exception("The provided model path does not exist")

    if os.path.isdir(args.model):
        for dirpath, dirnames, filenames in os.walk(args.model):
            if "model.joblib" in filenames:
                model_name = Path(dirpath).stem
                print(f"Loading model for {model_name}")
                model = joblib.load(dirpath)
                break
    elif os.path.isfile(args.model):
        model = joblib.load(args.model)
    
    if not model:
        raise Exception("Failed to load the model from the provided path")

    # Scoring
    df = pd.read_csv(args.testing_data_path)

    all_predictions = model.predict(df)

    # Writing out
    pd.DataFrame(all_predictions).to_csv(args.prediction)
