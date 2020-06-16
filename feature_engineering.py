# -*- coding: utf-8 -*-
"""
Created on Fri May 29 03:42:00 2020

@author: USER
"""

from pyhive import hive
import pandas as pd
import numpy as np
import re

# NLTK VADER for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
news_df.sort_values(by=['Date'],ascending=False,inplace=True)

# Drop duplicates
news_df.drop_duplicates(inplace=True)
news_df = news_df.reset_index(drop=True)

# Drop all rows not containing the word "oil"
for i in range(0, len(news_df)):
    if re.search(r'oil', news_df['News'][i], re.I) is not None:
        continue
    else:
        news_df.drop(i, inplace=True)

# Extract day and month
def get_day(x):
    return x.day

def get_month(x):
    return x.month

def get_weekday(x):
    return x.weekday()
    
news_df['day'] = news_df['Date'].apply(get_day)
news_df['month'] = news_df['Date'].apply(get_month)
news_df['weekday'] = news_df['Date'].apply(get_weekday)


news_df.to_csv(r'output/news_clean.csv',index=False)

#############################################################################

#                                 SENTIMENT                                 #

#############################################################################

# Load data to pandas
news_df = pd.read_csv(r'output/news_clean.csv')

# New words and values
new_words = {
    
    'doubled'       : 20,
    'tripled'       : 20,
    'undersupply'   : 20,
    
    'confidence'    : 10,
    'crush'         : 10,
    'jump'          : 10,
    'bull'          : 10,
    'spend'         : 10,
    'spends'        : 10,
    'invest'        : 10,
    'invests'       : 10,
    'boom'          : 10,
    
    'up'            : 5,
    'gain'          : 5,
    'gains'         : 5,
    'high'          : 5,
    'rise'          : 5,
    'rises'         : 5,
    'rising'        : 5,
    'revival'       : 5,
    'recovery'      : 5,
    'rally'         : 5,
    'surge'         : 5,
    'surges'        : 5,
    'beat'          : 5,
    'beats'         : 5,
    'profit'        : 5,
    'climb'         : 5,
    'climbs'        : 5,
    'buy'           : 5,
    'buys'          : 5,
    'rebound'       : 5,
    'rebounds'      : 5,
    
    'down'          : -5,
    'slump'         : -5,
    'tumble'        : -5,
    'misses'        : -5,
    'lose'          : -5,
    'losses'        : -5,
    
    'glut'          : -10,
    'trouble'       : -10,
    'fear'          : -10,
    'fears'         : -10,
    'fall'          : -10,
    'falls'         : -10,
    'bear'          : -10,
    'cheap'         : -10,
    'plunge'        : -10,
    'sell'          : -10,
    'sells'         : -10,
    'crash'         : -10,
    'crashes'       : -10,
    'plummet'       : -10,
    'downturn'      : -10,
    'bust'          : -10,
    
    
    'oversupply'    : -20,
    'bankruptcy'    : -20,
    'crisis'        : -20,
    'bail'          : -20,
    'bailout'       : -20,
    
}

# Instantiate the sentiment intensity analyzer with the existing lexicon
vader = SentimentIntensityAnalyzer()
# Update the lexicon
vader.lexicon.update(new_words)



scores = news_df['News'].apply(vader.polarity_scores)

# Convert the list of dicts into a DataFrame
scores_df = pd.DataFrame.from_records(scores)

# Join the DataFrames
news_df = news_df.join(scores_df)

news_df = news_df.drop(['News'], axis=1)

news_df.to_csv(r'output/news_sentiment.csv',index=False)

polarity_mean = news_df.groupby('Date', as_index=False)[['day','month','weekday','neg', 'neu', 'pos' , 'compound']].mean()

polarity_mean.to_csv(r'output/news_sentiment_mean.csv',index=False)

#############################################################################

#                               PRICE DATASET                               #

#############################################################################    
    
# Load data to pandas
cur.execute("SELECT * FROM raw_price")
raw_price=cur.fetchall()
price_df = pd.DataFrame(data=raw_price)    

price_df.columns = ['date', 'closing_price', 'open_price', 'daily_high', 'daily_low']

# Convert date string into datetime
price_df['date'] = pd.to_datetime(price_df['date'])
price_df.sort_values(by=['date'],ascending=False,inplace=True)


# Find difference between current and previous day prices
price_df['past_change'] = 0.0
for i in range (0,len(price_df)-1):
    price_df['past_change'][i] = price_df['closing_price'][i] - price_df['closing_price'][i+1]

price_df['future_change'] = 0.0
for i in range (0,len(price_df)-1):
    price_df['future_change'][i+1] = price_df['closing_price'][i] - price_df['closing_price'][i+1]

price_df = price_df

price_df.to_csv(r'output/price_features.csv', index=False)

#############################################################################

#                                  MERGE                                    #

#############################################################################

# Load data to pandas
polarity_mean = pd.read_csv(r'output/news_sentiment_mean.csv')
price_df = pd.read_csv(r'output/price_features.csv')

merged_df = pd.merge(polarity_mean,
                     price_df,
                     how='inner',
                     left_on=['Date'],
                     right_on=['date'])

merged_df.drop(['date'], axis=1, inplace = True)

merged_df.to_csv(r'output/dataset.csv',index=False)





