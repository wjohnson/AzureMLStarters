# imports
import os
import mlflow
import argparse

import pandas as pd
from pathlib import Path

from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder



if __name__ == "__main__":
    # We expect the command to provide a set of input parameters
    # including the hyperparameter values
    # This is different than running a normal sklearn hyperparameter tuning since the
    # below script effectively runs just one iteration of the hyperparameters
    parser = argparse.ArgumentParser()
    # These are the boilerplate ones that every Azure ML job should have
    parser.add_argument("--data", type=str)
    parser.add_argument("--random_state", type=int, default=42)
    parser.add_argument("--model_output", type=str, help="Path of output model")
    parser.add_argument("--test_data", type=str, help="Path of test data for reproducibility")
    # These are the hyperparameters you want to use
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--criterion", type=str, default="gini")
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--min_samples_split", type=int, default=2)
    parser.add_argument("--min_samples_leaf", type=int, default=1)
    parser.add_argument("--max_features", default="sqrt")

    args = parser.parse_args()

    model_hyperparameters = {
        "n_estimators": args.n_estimators,
        "criterion": args.criterion,
        "max_depth": args.max_depth,
        "min_samples_split": args.min_samples_split,
        "min_samples_leaf": args.min_samples_leaf,
        "max_features": args.max_features,
        "n_estimators": args.n_estimators,
    }

    # enable auto logging
    mlflow.autolog()
    # The sample data is semicolon delimited
    df = pd.read_csv(args.data, sep=";")

    # Prep data for training by removing irrelevant features and dependent variable (y)
    X = df.drop(["day","month","duration","campaign","pdays","previous","poutcome", "y"], axis=1)
    y = df["y"]

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=args.random_state
    )

    # Use a SKLearn Pipeline to make everything run together    
    pipe = Pipeline([
        # First step 
        (
            'encodeJob', 
            make_column_transformer(
                (
                    OneHotEncoder(),
                    ["job","marital","education","default","housing"]
                )
            )
        ),
        ('model', RandomForestClassifier(**model_hyperparameters))
        ]
    )
    pipe.fit(X_train, y_train)
    
    
    prediction = pipe.predict(X_test)
    report = classification_report(y_test, prediction)
    print(report)
    # Output the model and test data
    # write to local folder first, then copy to output folder

    mlflow.sklearn.save_model(pipe, "model")

    from distutils.dir_util import copy_tree

    # copy subdirectory example
    from_directory = "model"
    to_directory = args.model_output

    copy_tree(from_directory, to_directory)

    X_test.to_csv(Path(args.test_data) / "X_test.csv", index=False)
    y_test.to_csv(Path(args.test_data) / "y_test.csv", index=False)
