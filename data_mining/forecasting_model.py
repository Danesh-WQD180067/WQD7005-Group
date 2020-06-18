# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:27:32 2020

@author: USER
"""

import pandas as pd
from matplotlib import pyplot

from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


from math import sqrt
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

# Drop unnecessary columns
dataset.drop(['day', 'month', 'weekday',
              'open_price', 'daily_high', 'daily_low', 
              'future_change', 'past_change'], 
             axis=1, inplace = True)

dataset = dataset[['closing_price', 'neg', 'neu', 'pos', 'compound']]


# Normalize Features
values = dataset.values
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

# Save Scaler
scaler_filename = r'../pickles/scaler.gz'
joblib.dump(scaler, scaler_filename) 


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
train = values[:n_train_days, :]
test = values[n_train_days:, :]
# split into input and outputs
n_obs = n_days * n_features
train_X, train_y = train[:, :n_obs], train[:, -n_features]
test_X, test_y = test[:, :n_obs], test[:, -n_features]
print(train_X.shape, len(train_X), train_y.shape)
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_days, n_features))
test_X = test_X.reshape((test_X.shape[0], n_days, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

##############################################################################

#                               Design Model                                 #

##############################################################################

# design network
model = Sequential()

# 1st Layer
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))

# Output Layer
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

##############################################################################

#                                Train Model                                 #

##############################################################################

# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=30, 
                    validation_data=(test_X, test_y), 
                    verbose=2, shuffle=False)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

model.save('../pickles/model.h5')

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
# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -4:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

##############################################################################

#                                Plot Result                                 #

##############################################################################

# Plot prediction vs result
pyplot.plot(inv_y, color='green', label='Oil Price')
pyplot.plot(inv_yhat, color='red', label='Predicted Oil Price')
pyplot.legend()
pyplot.title('Oil Price Prediction Results')
pyplot.xlabel('time')
pyplot.ylabel('Oil Price')