# CS6400 Project README

## Requirements

This project requires the following packages to run:

- alpaca-py (>=0.33.1)
- numpy (>=1.26.2)
- pandas (>=2.2.3)
- scikit-learn (>=1.5.2)
- scipy (>=1.12.0)
- torch (>=2.5.1)
- transformers (>=4.46.3)
- tqdm (>=4.67.1)

## Sentiment Extraction

This section provides information on running code to extract sentiment from the desired dataset.

`tweet_analyzer.py` is the file to run for calculating sentiment. On line 26, the function `pd.read_csv()` takes an input, and here you should replace the parameter with your dataset. The function expects a .CSV file, and ensure your dataset has a column labeled "Created At" to store the timestamp.

On line 50, the function `df.to_csv()` expects an output file parameter, so add desired name of your output file which holds the determined sentiment.

Depending on the size of the dataset, this step will consume the most of the computation time.

## Prediction Model

Below are descriptions for the various parameters and requirements for running the files related to the prediction model. Each of the following files should be run in order of appearence here.

### Data Collection

The first file to run is `stock_data_grabber`. This is a simple file that interfaces with the Alpaca API to obtain historical stock data. 
In order to use the API, one must generate public and private keys. An account must be made in order to obtain the keys, but afterwards they can be generated rather quickly. Information for this step is detailed [here](https://docs.alpaca.markets/docs/getting-started-with-alpaca-market-data).

In the `stock_data_grabber.py` file, the stock to retrieve data for, as well as the interested timeframe, can all be changed by altering the parameters for the `StockBarsRequest()` object. The desired stock can be changed via the *symbol_or_symbols* parameter. *timeframe* controls the intervals of information to collect, on a hourly, daily, etc. basis. *start* and *end* parameters signal the dates to bound the data collection.
If you want to collect information on multiple stocks, you can use the *symbol_or_symbols* parameter, passing in a list of tocker symbols you want to collect information for. For instance, to collect both Bitcoin and the S&P 500, you can use `symbol_or_symbols=["SPY", "BTC/USD"]`

### Data Transformation

The next file to run is the `data_handler.py` file. This file is used to find directional changes based on the stock data, as well as aggregate the sentiment extracted from `tweet_analyzer.py`.

In the main function, all you need to do is pass in the appropriate .CSV files to the functions. `retrieve_data()` loads the stock data acquired earlier into the file to calculate directional change, and `aggreaget_sentiment()` takes a data file with sentiment values, built after running `tweet_analyzer.py`.

The handler functions will each create a file to store the transformed data. The aggregate sentiment will be stored in `aggregate_sent.csv`, and the calculated directional changes for each trading day are stored in `dc_trends.csv`.
Addtionally, this file will output `combined_result.csv`, which is a convenience file that has both aggregate sentiment and determined directional change trend listed per each hour within the date range used in `stock_data_grabber.py`.

### Logistic Regression Classifier

The last file, `classifier.py` is used to create and train a logisitic regression classifier for prediction problems. Given direction change trends and aggregate sentiment, the classifier should determine if an unknown day will have an upward, downward, or stagnate trend, based on the hourly sentiment.

If you changed the names of the output files from the Data Transformation step, then the names of .CSV files must also be changed in the main function for `classifier.py`. The code expects `aggregate_sent.csv` and `dc_trends.csv` in order to load this data into the classifier. Change this parameters accordingly if you made any changes to the prior code.

After the model is done training, it will be exposed to the testing set, from which an Accuracy and Macro-F1 score will be determined. Both of these values will be output to the console for future analysis.
