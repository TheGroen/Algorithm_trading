# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:19:44 2021

@author: JacobsEb
"""
import MetaTrader5 as mt5
import pandas as pd  
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np 
from scipy.signal import argrelextrema as scarg
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import time

account_no1 = 28829869
account_password_no1 = "DemoStrategy101"
name = "BTCUSD"

mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1)

if not mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1):
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())

ea_magic_number = 888999000 # if you want to give every bot a unique identifierz

def Learn_market (symbol,timeframe):
    symbol_rates = mt5.copy_rates_from(symbol,timeframe , datetime.now() , 1000)
    
    # create DataFrame out of the obtained data
    ticks_rates = pd.DataFrame(symbol_rates)
    ticks_rates['time']=pd.to_datetime(ticks_rates['time'], unit= 's')   
    
    #finding where the minimum and maximum values of the symbol info is
    min_value_places = scarg(symbol_rates['open'],np.less,order=5)
    max_value_places = scarg(symbol_rates['open'],np.greater,order=5)
    time=symbol_rates['time']
    open=symbol_rates['open']
    
    plt.plot(symbol_rates['time'],symbol_rates['open'],time[max_value_places],open[max_value_places],'or',time[min_value_places],open[min_value_places],'ob' )
    
    #creating an array to store places for learning
    #clasification learning     two arrays are formed one is buying and one is selling
    learner_array_buy = np.zeros(np.size(ticks_rates['close']))
    learner_array_sell = np.zeros(np.size(ticks_rates['close']))
    learner_array_buy[min_value_places] = 1
    learner_array_sell[max_value_places] = 1
    
    marketData= np.array(symbol_rates['open'])
    marketData=marketData.reshape(-1,1)
    
    X_train, X_test, y_train, y_test = train_test_split(marketData, learner_array_buy)
    
    cls_buy = SVC().fit(X_train,y_train)
    
    
    accuracy_train =  accuracy_score(y_train, cls_buy.predict(X_train))
    accuracy_test =  accuracy_score(y_test, cls_buy.predict(X_test))
    
    print('\nTrain Accuracy:{: .2f}%'.format(accuracy_train*100))
    print('Test Accuracy:{: .2f}%'.format(accuracy_test*100))
    
    X_train, X_test, y_train, y_test = train_test_split(marketData, learner_array_sell)
    
    cls_sell = SVC().fit(X_train,y_train)
    
    
    accuracy_train =  accuracy_score(y_train, cls_sell.predict(X_train))
    accuracy_test =  accuracy_score(y_test, cls_sell.predict(X_test))
    
    print('\nTrain Accuracy:{: .2f}%'.format(accuracy_train*100))
    print('Test Accuracy:{: .2f}%'.format(accuracy_test*100))
    
    return cls_buy,cls_sell

def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info

def open_trade(action, symbol, lot, sl_points, tp_points, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    point = mt5.symbol_info(symbol).point

    buy_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": 0,# price - sl_points * point,
        "tp": 0,#price + tp_points * point,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "sent by python",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    # send a trading request
    result = mt5.order_send(buy_request)        
    return result, buy_request 

def close_trade(action, buy_request, result, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
    symbol = buy_request['symbol']
    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    position_id=result.order
    lot = buy_request['volume']

    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    # send a close request
    result=mt5.order_send(close_request)

# example of filling orders with these functions.
# result, buy_request = open_trade('buy', 'USDJPY', 0.1, 50, 50, 10)
# close_trade('sell', buy_request, result, 10)

#create seed model 
model_buy,model_sell = Learn_market(name,mt5.TIMEFRAME_M5 );
storingMat=[]

# while True:
#     #get new market data 
while True: 
    symbol_set_new= symbol_rates = mt5.copy_rates_from(name,mt5.TIMEFRAME_M5 , datetime.now() , 10)
    symbol_set_new = np.array(symbol_set_new).reshape(-1,1)
    prediction_values_buy = model_buy.predict(symbol_set_new['open'])
    prediction_values_sell = model_sell.predict(symbol_set_new['open'])
    print('prediction for buy',prediction_values_buy)
    print('prediction sell', prediction_values_sell)
    storingMat.append([datetime.now(), prediction_values_buy, prediction_values_sell]);
    time.sleep(60*5)

