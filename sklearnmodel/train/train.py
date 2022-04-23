import numpy as np
from sklearn.linear_model import LinearRegression
import joblib


if __name__ == "__main__":

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    # y = 1 * x_0 + 2 * x_1 + 3
    y = np.dot(X, np.array([1, 2])) + 3

    reg = LinearRegression().fit(X, y)

    with open('./outputs/model.joblib', 'wb') as fp:
        joblib.dump(reg, fp)
