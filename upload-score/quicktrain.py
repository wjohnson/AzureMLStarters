import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

if __name__ == "__main__":
    df = pd.DataFrame([
        {"a":2, "b": 4, "c":6},
        {"a":3, "b": 1, "c":4},
        {"a":5, "b": 2, "c":7},
        {"a":7, "b": 3, "c":10},
        {"a":10, "b": 4, "c":14},
        {"a":12, "b": 5, "c":17},
        {"a":14, "b": 6, "c":20},
        {"a":1, "b": 1, "c":2},
        {"a":2, "b": 2, "c":4},
        {"a":3, "b": 3, "c":6}
    ])
    X = df.iloc[:, 0:2]
    y = df.c

    lr = LinearRegression().fit(X, y)

    joblib.dump(lr,'./model/model.joblib')