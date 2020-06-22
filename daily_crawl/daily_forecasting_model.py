# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:27:32 2020

@author: USER
"""

import pandas as pd

from sklearn.externals import joblib
from keras.models import load_model

from datetime import datetime
from numpy import concatenate

# convert series to supervised learning
def series_to_supervised(df, n_in=1, n_out=1, dropnan=True):
    data = df.values
    n_vars = 1 if type(data) is list else data.shape[1]

    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [( df.columns[j] + ' (t-%d)' % (i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [( df.columns[j] + ' (t)') for j in range(n_vars)]
        else:
            names += [( df.columns[j] + ' (t+%d)' % (i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

##############################################################################

#                               Prepare Data                                 #

##############################################################################

# load dataset
dataset = pd.read_csv(r'output/dataset.csv', header=0, index_col=0)

dataset = dataset[['closing_price', 'neg', 'neu', 'pos', 'compound']]

# Get only past 30 days
dataset = dataset.tail(31)

lastdate = dataset.tail(1).index.item()
lastdate = datetime.strptime(lastdate, '%Y-%m-%d')

lastprice = dataset.tail(1).closing_price.item()

# Load Scaler
# And now to load...
scaler_filename = r'../pickles/scaler.gz'
scaler = joblib.load(scaler_filename) 

# Normalize Features
values = dataset.values
scaled = scaler.fit_transform(values)

dataset = pd.DataFrame(scaled)
dataset.columns = ['closing_price', 'neg', 'neu', 'pos', 'compound']

n_days = 30
n_features = 5

# frame as supervised learning
reframed = series_to_supervised(dataset, 30, 1)
# drop columns we don't want to predict
# reframed.drop(['neg (t)', 'pos (t)'], axis=1, inplace=True)
print(reframed.head())


# split into train and test sets
values = reframed.values
n_train_days = len(values) - 30

test = values[:, :]
# split into input and outputs
n_obs = n_days * n_features

test_X, test_y = test[:, :n_obs], test[:, -n_features]
# reshape input to be 3D [samples, timesteps, features]
test_X = test_X.reshape((test_X.shape[0], n_days, n_features))

##############################################################################

#                                 Test Model                                 #

##############################################################################

model = load_model('../pickles/model.h5')

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_days*n_features))
# invert scaling for forecast
inv_yhat = concatenate((yhat, test_X[:, -4:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

##############################################################################

#                                Save Result                                 #

##############################################################################

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, DateTime, MetaData

engine = create_engine('sqlite:///../pickles/predictions.db', echo = True)
meta = MetaData()

predictions = Table(
   'predictions', meta, 
   Column('id', Integer, primary_key = True), 
   Column('p_date', DateTime),
   Column('p_price', Float(asdecimal=False)), 
   Column('f_price', Float(asdecimal=False)), 
)

meta.create_all(engine)

ins = predictions.insert()
ins = predictions.insert().values(p_date = lastdate, p_price=lastprice, f_price = inv_yhat)
conn = engine.connect()
result = conn.execute(ins)