"""
Created on Saturday, 08 May 2021

@author: Hendrik T. Burger
"""

# Importing the required attributes.
# import tensorflow as tf
import pandas as pd
import numpy as np

from statistics import mean

# Imports the stock data from the specified file.
df = pd.read_csv('F:htb_stock_data.csv')


# Calculate the log return for the closing price.
df['Returns'] = df.Close.pct_change()
df['Log Rtn'] = np.log1p(df['Returns'])

# Calculates the change in closing prices.
df['Change'] = df.Close.diff()

# Determine the gains.
for x in df.index:
    if df.loc[x, 'Change'] < 0:
        df.loc[x, 'Gain'] = 0
    else:
        df.loc[x, 'Gain'] = df.loc[x, 'Change']

# Determine the losses.
for x in df.index:
    if df.loc[x, 'Change'] > 0:
        df.loc[x, 'Loss'] = 0
    else:
        df.loc[x, 'Loss'] = -df.loc[x, 'Change']

# Calculating the Relative Strength Index
avggain = []
gn = df['Gain']

# Calculates the smoothing constant for a 14 period RSI.
scrsi = 2 / (14 + 1)

# Creating the Average Gain value list.
# Zeros the first thirteen values in the list.
for m in range(14):
    avggain.append(0)
avggain.append(mean(gn[1:15]))

# Calculates the average gain using exponential moving averages.
for n in range(len(df) - 15):
    x = avggain[n + 14] + (gn[n + 15] - avggain[n + 14]) * scrsi
    avggain.append(x)

# Add the calculated average loss to the dataframe.
df['Avg Gain'] = avggain
avgloss = []
gl = df['Loss']

# Creating the Average Loss value list.
# Zeros the first thirteen values in the list.
for m in range(14):
    avgloss.append(0)
avgloss.append(mean(gl[1:15]))

# Calculates the average loss using exponential moving averages.
for n in range(len(df) - 15):
    x = avgloss[n + 14] + (gl[n + 15] - avgloss[n + 14]) * scrsi
    avgloss.append(x)

# Add the calculated average loss to the dataframe.
df['Avg Loss'] = avgloss

# Calculating the Relative Strength and appending to its list.
rs = []
for o in range(len(df)):
    if avgloss[o] == 0:
        rs.append(0)
    else:
        rs.append(avggain[o] / avgloss[o])

# Add the calculated relative strength to the dataframe.
df['RS'] = rs

# Calculating the Relative Strength Index and appending to the RSI list.
rsi = []
for q in range(len(df)):
    rsi.append(100 - (100 / (1 + rs[q])))

# Add the calculated RSI to the dataframe.
df['RSI'] = rsi

# Calculating the smoothing constant for 12 periods.
scmacd12 = 2 / (12 + 1)
# Calculating the smoothing constant for 26 periods.
scmacd26 = 2 / (26 + 1)

# Calculating the Exponential Moving Average for 12 periods.
clpr = df['Close']
# Zeros the first eleven values in the EMA list.
ema12 = []
for r in range(11):
    ema12.append(0)

ema12.append(mean(clpr[1:12]))

# Calculates the EMA.
for s in range(len(df) - 12):
    x = ema12[s + 11] + (clpr[s + 12] - ema12[s + 11]) * scmacd12
    ema12.append(x)

# Calculating the Exponential Moving Average for 26 periods.
# Zeros the first twenty-six values in the EMA list.
ema26 = []
for t in range(25):
    ema26.append(0)

ema26.append(mean(clpr[1:26]))

# Calculates the EMA.
for u in range(len(df) - 26):
    x = ema26[u + 25] + (clpr[u + 26] - ema26[u + 25]) * scmacd26
    ema26.append(x)

# Add to the dataframe.
df['EMA12'] = ema12
df['EMA26'] = ema26

# Create the Moving Average Converging Diverging line value list.
macdline = []
# Zero the first twenty-five values in the list.
for v in range(25):
    macdline.append(0)

# Calculates the MACD line values.
for w in range(len(df) - 25):
    x = ema12[w + 25] - ema26[w + 25]
    macdline.append(x)

# Add the MACD line to the dataframe.
df['MACD'] = macdline

# Calculate the %K of the Stochastic Oscillator
# Calculate the rolling 14 period high maximum.
df['HighMax'] = df.High.rolling(14).max()

# Calculate the rolling 14 period lowest minimum.
df['LowMin'] = df.Low.rolling(14).min()

# Calculate the percentage K.
df['%K'] = (df['Close'] - df['LowMin']) / (df['HighMax'] - df['LowMin'])

# If statement to determine the BHS signal.
# BUY = 2, HOLD =1, SELL = 0
bhs = []
bhs.append(0)
bhs.append(0)

for ag in range(len(df) - 2):
    if clpr[ag] < clpr[ag + 1] and clpr[ag + 1] < clpr[ag + 2] and clpr[ag + 2] < clpr[ag + 3]:
        bhs.append(0)
    else:
        if clpr[ag] > clpr[ag + 1] and clpr[ag + 1] > clpr[ag + 2]:
            bhs.append(2)
        else:
            bhs.append(1)

# Writing the BHS to the dataframe.
df['BHS'] = bhs

# Replace all NaN with zeros.
df.fillna(0, inplace=True)

# Identifying the target values.
target = df['Close']

# Drop unused columns.
data = df.drop(['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Change', 'Gain', 'Loss', 'Avg Gain',
                'Avg Loss', 'RS', 'EMA12', 'EMA26', 'HighMax', 'LowMin'], axis=1)

for ab in range(25):
    data = data.drop(ab)

# Create the target array.
target = target.values
data = data.values

print(data.shape)
