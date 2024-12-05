import csv
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

def read_files(datafile):
    sentiment = {}
    ground_truth = {}
    with open(datafile) as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            sentiment[line[1]] = line[3]
            ground_truth[line[1]] = line[2]
    sentiment.pop('Created At')
    ground_truth.pop('Created At')
    return sentiment, ground_truth

def window_transform(sentiment_df, dc_df):
    constant = 16   # hours NYSE is open each day
    sent_series = np.array(sentiment_df['Sentiment'])
    dc_series = np.array(dc_df['trend'])
    
    X: list[list[int]] = []
    for i in range(len(dc_series)):
        X.append(sent_series[i : i+constant])
    X = np.array(X)
    print(X.shape)

    Y: list[list[int]] = []
    for i in range(len(dc_series)):
        Y.append(dc_series[i])
    Y = np.array(Y)
    print(Y)
    return X, Y

def log_reg_classifier(X, Y):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, test_size=0.2)
    print("Array shapes:\n X_train = {}\n y_train = {}\n X_test = {}\n y_test = {}".format(x_train.shape, y_train.shape, x_test.shape, y_test.shape))
    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)

    y_pred = classifier.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    return acc, macro_f1


if __name__ == '__main__':
    sentiment = pd.read_csv('aggregate_sent.csv')
    dc_trends = pd.read_csv('dc_trends.csv')
    X, Y = window_transform(sentiment, dc_trends)
    acc, macro_f1 = log_reg_classifier(X, Y)
    print(f"Accuracy: {acc}")
    print(f"Macro F1: {macro_f1}")