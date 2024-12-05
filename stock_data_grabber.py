import time
import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.enums import AssetClass
from alpaca.data.timeframe import TimeFrame
from alpaca.data.timeframe import TimeFrameUnit
from datetime import datetime

public_key = 'PK3F163QBGZS637MBOUA'
private_key = 'gh2qBAHzJq8TGxed4iGvfQBtnpIh9zXIonnkT5OB'

stock_client = StockHistoricalDataClient(public_key, private_key)
stock_request_params = StockBarsRequest(symbol_or_symbols='SPY', timeframe=TimeFrame.Day, start=datetime(2018, 7, 9), end=datetime(2018, 7, 19))
bars = stock_client.get_stock_bars(stock_request_params)
bars.df.to_csv('sp500-df.csv')
time.sleep(0.31)