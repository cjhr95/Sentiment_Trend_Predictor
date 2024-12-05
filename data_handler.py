import numpy as np
import pandas as pd
from dateutil import parser
from datetime import datetime

def retrieve_data(filename):
    data = pd.read_csv(filename)
    return data

def window_transform(dataframe):
    constant = 16   # length of time series
    series = np.array(dataframe['close'])
    X: list[list[int]] = []
    Y: list[list[int]] = []
    for i in range(len(series) - constant):
        X.append(series[i : i+constant])
        Y.append(series[i+constant : i+constant+1])
    X = np.array(X)
    Y = np.array(Y)
    return X, Y

def aggregate_sentiment(sentiment_file):
    sent_data = pd.read_csv(sentiment_file)
    #print(sent_data.head())
    for index, row in sent_data.iterrows():
        new_date = parser.parse(row['Created At'])
        if new_date.hour < 8:   # NYSE isn't open before 8am
            sent_data.loc[index, 'Created At'] = None
        elif new_date.month != 7 or new_date.day <= 8:
            sent_data.loc[index, 'Created At'] = None
        else:
            new_date = datetime(new_date.year, new_date.month, new_date.day, new_date.hour, minute=0, second=0, microsecond=0)
            sent_data.loc[index, ['Created At']] = new_date
    sent_data = sent_data.groupby('Created At')['Sentiment'].mean()
    sent_data.to_csv('aggregate_sent.csv', index=True)
    return sent_data

def determine_dc(stock_data):
    dc_dict = {}
    for index, row in stock_data.iterrows():
        price_diff = float(stock_data.loc[index, 'close']) - float(stock_data.loc[index, 'open'])
        print(f"{price_diff} : {float(stock_data.loc[index, 'close']) * 0.001}")
        if abs(price_diff) > float(stock_data.loc[index, 'close']) * 0.001 and price_diff < 0:
            dc_dict[stock_data.loc[index, 'timestamp']] = 'down_trend'
        elif abs(price_diff) > float(stock_data.loc[index, 'close']) * 0.001 and price_diff > 0:
            dc_dict[stock_data.loc[index, 'timestamp']] = 'up_trend'
        else:
            dc_dict[stock_data.loc[index, 'timestamp']] = 'no_trend'

    timestamps = []
    trends = []
    for key, item in dc_dict.items():
        key_date = parser.parse(key)
        timestamps.append(datetime(key_date.year, key_date.month, key_date.day, key_date.hour, minute=0, second=0, microsecond=0))
        trends.append(item)
    dc_frame = pd.DataFrame()
    dc_frame.insert(0, 'Created At', timestamps)
    dc_frame.insert(1, 'trend', trends)
    #print(dc_frame.head())
    dc_frame.to_csv('dc_trends.csv')
    return dc_frame


if __name__ == '__main__':
    stock_data = retrieve_data('sp500-df.csv')
    dc_data = determine_dc(stock_data)
    print(dc_data.head())
    print("----------------------------------------------")
    sentiment_data = aggregate_sentiment('TWEET-07_09-07_18_sentiment_cnlp.csv')
    print(sentiment_data.head())
    print("----------------------------------------------")
    # result = pd.merge(dc_data, sentiment_data, on='Created At')
    # print(result.to_string())
    # result.to_csv('combined_result.csv')
    
