# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:32:10 2021

@author: JacobsEb
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from datetime import datetime

#setting up MT5 to start reading information from the market 
Symbol_Trade = "GBPUSD"
TimeFrame = mt5.TIMEFRAME_M15
account_no1 = 28829869
account_password_no1 = "DemoStrategy101"

mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1)

if not mt5.initialize(login=account_no1, server="Exness-MT5Trial",password=account_password_no1):
    print("initialize() failed")
    mt5.shutdown()
    
print(mt5.terminal_info())  

symbol_rates = mt5.copy_rates_from(Symbol_Trade,mt5.TIMEFRAME_H1 , datetime.now() , 100)

# create DataFrame out of the obtained data
ticks_rates = pd.DataFrame(symbol_rates)
ticks_rates['time']=pd.to_datetime(ticks_rates['time'], unit= 's')   
