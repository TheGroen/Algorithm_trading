# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:53:43 2021

@author: JacobsEb
"""
import numpy as np 
import pandas as pd 
import MetaTrader5 as mt5
from datetime import datetime 
from scipy.signal import argrelextrema as scarg
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from sklearn.metrics import classification_report,confusion_matrix

account_no1 = 28829869
account_password_no1 = "DemoStrategy101"
name = "BTCUSD"

mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1)

if not mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1):
    print("initialize() failed")
    mt5.shutdown()
    

#def Learn_market (symbol,timeframe):

symbol_rates = mt5.copy_rates_from(name,mt5.TIMEFRAME_H1 , datetime.now() , 100)

# create DataFrame out of the obtained data
ticks_rates = pd.DataFrame(symbol_rates)
ticks_rates['time']=pd.to_datetime(ticks_rates['time'], unit= 's')   

#finding where the minimum and maximum values of the symbol info is
min_value_places = scarg(symbol_rates['open'],np.less,order=1)
max_value_places = scarg(symbol_rates['open'],np.greater,order=1)
time=symbol_rates['time']
open=symbol_rates['open']

plt.plot(symbol_rates['time'],symbol_rates['open'],time[max_value_places],open[max_value_places],'or',time[min_value_places],open[min_value_places],'ob' )

#creating an array to store places for learning
#clasification learning     two arrays are formed one is buying and one is selling
learner_array_buy = np.zeros(np.size(ticks_rates['close']))
learner_array_sell = np.zeros(np.size(ticks_rates['close']))
learner_array_buy[min_value_places] = 1
learner_array_sell[max_value_places] = 1

y = learner_array_buy
X=pd.DataFrame(symbol_rates)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=101)

model = Sequential()

# https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw

model.add(Dense(units=30,activation='relu'))

model.add(Dense(units=15,activation='relu'))


model.add(Dense(units=1,activation='sigmoid'))

# For a binary classification problem
model.compile(loss='binary_crossentropy', optimizer='adam')


model.fit(x=X_train, 
          y=y_train, 
          epochs=600,
          validation_data=(X_test, y_test), verbose=1
          )

model_loss = pd.DataFrame(model.history.history)

model = Sequential()
model.add(Dense(units=30,activation='relu'))
model.add(Dense(units=15,activation='relu'))
model.add(Dense(units=1,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')

early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=25)

model.fit(x=X_train, 
          y=y_train, 
          epochs=600,
          validation_data=(X_test, y_test), verbose=1,
          callbacks=[early_stop]
          )

model = Sequential()
model.add(Dense(units=30,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(units=15,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(units=1,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')


model.fit(x=X_train, 
          y=y_train, 
          epochs=600,
          validation_data=(X_test, y_test), verbose=1,
          callbacks=[early_stop]
          )
model_loss = pd.DataFrame(model.history.history)
model_loss.plot()