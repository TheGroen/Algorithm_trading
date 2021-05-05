"""
Created on Saturday, 1 May 2021

@author: Hendrik T. Burger
"""

import pandas as pd
import numpy as np

# Imports the stock data from the specified file.
df = pd.read_csv('F:htb_stock_data.csv')

# Adjusts the data from the CSV data file to the appropriate format.
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')

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

# Calculate the moving average gain for 14 periods.
df['Avg Gain'] = df.Gain.rolling(14).mean()

# Calculate the moving average loss for 14 periods.
df['Avg Loss'] = df.Loss.rolling(14).mean()

# Calculate the relative strength.
"""for y in df.index:
  if df.loc[y, 'Avg Loss'] == 0:
    df.loc[y, 'RS'] = 0
  else:
    df.loc[y, 'RS'] = df.loc[y, 'Avg Gain'] / df.loc[y, 'Avg Loss']"""

# Calculating the Relative Strength Index.
# df['RSI'] = (100 - (100 / (1 + df['RS'])))

# Calculate the moving average loss for 14 periods.
# df['Avg Loss'] = df.Loss.rolling(14).mean()

# Calculate the exponential moving average for the closing price with a 12 period.
# df['EMA12'] = df.Close.ewm(com=0).mean()

# Calculate the exponential moving average for the closing price with a 26 period.
# df['EMA26'] = df.Close.ewm(com=0).mean()

# Calculate the Moving Average Converging Diverging.
# df['MACD'] = df['EMA12'] - df['EMA26']




"""# Creates the lists used in the calculation of the various parameters.
change, gain, loss, avggain, avgloss, rs, rsi, ema12, ema26, macdline, perck, bhs = [], [], [], [], [], [], [], [], [],\
                                                                                    [], [], []

# Calculating the smoothing constant for 12 periods.
scmacd12 = 2 / (12 + 1)
# Calculating the smoothing constant for 26 periods.
scmacd26 = 2 / (26 + 1)

# Calculating the Exponential Moving Average for 12 periods.
# Zeros the first eleven values in the EMA list.
for r in range(11):
    ema12.append(0)

ema12.append(mean(loss[1:12]))

# Calculates the EMA.
for s in range(len(df) - 12):
    x = ema12[s + 11] + (loss[s + 12] - ema12[s + 11]) * scmacd12
    ema12.append(x)

# Calculating the Exponential Moving Average for 26 periods.
# Zeros the first twenty-six values in the EMA list.
for t in range(25):
    ema26.append(0)

ema26.append(mean(loss[1:26]))

# Calculates the EMA.
for u in range(len(df) - 26):
    x = ema26[u + 25] + (loss[u + 26] - ema26[u + 25]) * scmacd26
    ema26.append(x)

# Create the Moving Average Converging Diverging line value list.
# Zero the first twenty-five values in the list.
for v in range(25):
    macdline.append(0)

# Calculates the MACD line values.
for w in range(len(df) - 25):
    x = ema12[w + 25] - ema26[w + 25]
    macdline.append(x)

# Creating the Stochastic Oscillator list.
# Create the maximum high value list.
maxso = []
for ab in range(len(df) - 13):
    maxso01 = []
    for ac in range(ab, ab + 14):
        maxso01.append(df.loc[ac][2])
    maxso.append(max(maxso01))

# Create the minimum low value list.
minso = []
for ad in range(len(df) - 13):
    minso01 = []
    for ae in range(ad, ad + 14):
        minso01.append((df.loc[ae][3]))
    minso.append(min(minso01))

# Zero the first fourteen values in the list.
for af in range(13):
    perck.append(0)

# Calculate the SO signal line
for af in range(len(df) - 15):
    perck.append((df.loc[af + 14][4] - minso[af]) / (maxso[af] - minso[af]))
perck.append(0)
perck.append(0)

# Determining the Buy, Hold and Sell signal.
# Zero the first two values in the list.
bhs.append(0)
bhs.append(0)

# If statement to determine the BHS signal.
for ag in range(len(df) - 2):
    if df.loc[ag + 2][4] > df.loc[ag][4] and df.loc[ag + 2][4] > df.loc[ag + 1][4]:
        bhs.append('BUY')
    else:
        if df.loc[ag + 2][4] < df.loc[ag][4] and df.loc[ag + 2][4] < df.loc[ag + 1][4]:
            bhs.append('SELL')
        else:
            bhs.append('HOLD')"""

# Replace all NaN with zeros.
df.fillna(0, inplace = True)

# Test the results.
print(df[10:30])
