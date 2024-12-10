# 
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm
import torch


def analyze_sentiment_with_score(tweet):
    try:
        result = sentiment_pipeline(tweet[:512])[0]  
        label = result['label']
        score = result['score']
        return label, score
    except Exception as e:
        return "Error", 0.0

# for readability
label_map = {
    "LABEL_0": "-1", # negative
    "LABEL_1": "0",  # neutral
    "LABEL_2": "1"   # positive
}

# import data
# ! copy your input filepath here
df = pd.read_csv("TWEET-07_09_2018-07_18_2018.csv")

print(df.head())


model_name = "cardiffnlp/twitter-roberta-base-sentiment"
# model_name = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1) 

# adds a progress bar
tqdm.pandas()
# add columns
df[['Sentiment', 'Confidence']] = df['text'].progress_apply(
    lambda x: pd.Series(analyze_sentiment_with_score(x))
)

# apply mapping
df['Sentiment'] = df['Sentiment'].map(label_map)

#! copy your output filepath here
df.to_csv("TWEET-07_09-07_18_sentiment_cnlp.csv", index=False)
print(df.head())
