import pandas as pd

if __name__ == "__main__":
    df = pd.DataFrame([
        {"a":2, "b": 4},
        {"a":3, "b": 1},
        {"a":5, "b": 2},
        {"a":7, "b": 3},
        {"a":10, "b": 4},
        {"a":12, "b": 5},
        {"a":14, "b": 6},
        {"a":1, "b": 1},
        {"a":2, "b": 2},
        {"a":3, "b": 3}
    ])
    df.to_csv("./quickdata.csv", index=False, header=True)
