# -*- coding: utf-8 -*-
"""
Created on Fri May 29 03:42:00 2020

@author: USER
"""

from pyhive import hive
import pandas as pd
import numpy as np
import re

# For sentiment analysis
from textblob import TextBlob

# Create Hive Cursor
host_name = "localhost"
port = 10000
conn = hive.Connection(host=host_name, port=port, auth='NOSASL')
cur = conn.cursor()


#############################################################################

#                               NEWS DATASET                                #

#############################################################################

# Load data to pandas
cur.execute("SELECT * FROM raw_news")
raw_news=cur.fetchall()
news_df=pd.DataFrame(data=raw_news)

news_df.columns = ['Date', 'News']

# Remove empty rows
news_df['News'].replace('', np.nan, inplace=True)
news_df = news_df.dropna(subset=['News'])

# Drop unnecessary "time" values in the date column
news_df['Date'].replace(['^(.*?)(PM|AM)'], [''], regex=True, inplace=True)
news_df['Date'].replace(['\s(.*)'], [''], regex=True, inplace=True)

# Convert date string into datetime
news_df['Date'] = pd.to_datetime(news_df['Date'])
news_df.sort_values(by=['date'],ascending=False,inplace=True)

# Drop duplicates
news_df.drop_duplicates(inplace=True)
news_df = news_df.reset_index(drop=True)

# Drop all rows not containing the word "oil"
for i in range(0, len(news_df)):
    if re.search(r'oil', news_df['News'][i], re.I) is not None:
        continue
    else:
        news_df.drop(i, inplace=True)


news_df.to_csv(r'output/news_clean.csv',index=False)

#############################################################################

#                               NEWS DATASET                                #

#############################################################################

news_df['sentiment_polarity'] = 0.0
news_df['sentiment_subjectivity'] = 0.0

# Drop duplicates
news_df.drop_duplicates(inplace=True)
news_df = news_df.reset_index(drop=True)

for i in range(0,len(news_df)):
    blob = TextBlob(news_df['News'][i])
    Sentiment = blob.sentiment
    news_df['sentiment_polarity'][i] = Sentiment.polarity
    news_df['sentiment_subjectivity'][i] = Sentiment.subjectivity


news_df = news_df.drop(['News'], axis=1)

news_df.to_csv(r'output/news_sentiment.csv',index=False)

polarity_mean = news_df.groupby('Date', as_index=False)['sentiment_polarity'].mean()

polarity_mean.to_csv(r'output/news_sentiment_mean.csv',index=False)

#############################################################################

#                               NEWS DATASET                                #

#############################################################################    
    
# Load data to pandas
cur.execute("SELECT * FROM raw_price")
raw_price=cur.fetchall()
price_df=pd.DataFrame(data=raw_price)    

price_df.columns = ['date', 'closing_price', 'open_price', 'daily_high', 'daily_low']

# Convert date string into datetime
price_df['date'] = pd.to_datetime(price_df['date'])
price_df.sort_values(by=['date'],ascending=False,inplace=True)


# Find difference between current and previous day prices
price_df['intraday_change'] = 0.0
for i in range (0,len(price_df)-1):
    price_df['intraday_change'][i] = price_df['closing_price'][i+1] - price_df['closing_price'][i]

# Extract day and month
def get_day(x):
    return x.day

def get_month(x):
    return x.month

def get_weekday(x):
    return x.weekday()
    

price_df['day'] = price_df['date'].apply(get_day)
price_df['month'] = price_df['date'].apply(get_month)
price_df['weekday'] = price_df['date'].apply(get_weekday)


#############################################################################

#                               MERGE                                #

#############################################################################

merged_df = pd.merge(polarity_mean,
                     price_df,
                     how='left',
                     left_on=['Date'],
                     right_on=['date'])

polarity_mean.to_csv(r'output/dataset.csv',index=False)





