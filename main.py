import pandas as pd
import numpy as np
from sklearn.svm import SVC


def SVCfit(x_train, y_train):
    clf = SVC(gamma="auto")
    clf.fit(x_train, y_train)

    print(clf.score(x_train, y_train))

    return clf


if __name__ == "__main__":
    df = pd.read_csv("data/train.csv")

    df = df.dropna()

    train_df = df[df["year"] != 2020]
    test_df = df[df["year"] == 2020]

    x_train = train_df.drop(["year", "state", "inc_appr", "inc_win"], axis=1).to_numpy()
    y_train = train_df["inc_win"].to_numpy()

    x_test = test_df.drop(["year", "state", "inc_appr", "inc_win"], axis=1).to_numpy()
    y_test = test_df["inc_win"].to_numpy()

    clf = SVCfit(x_train, y_train)

    print(clf.predict(x_test))
    print(y_test)
    test_df.insert(7, "pred", clf.predict(x_test), True)

    test_df.to_csv("data/2020pred.csv")
