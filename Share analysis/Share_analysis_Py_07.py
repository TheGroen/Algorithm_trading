"""
Created on Wed Apr 21 2021

@author: Hendrik T. Burger
"""

import pandas as pd
from statistics import mean

# Imports the stock data from the specified file.
df = pd.read_csv('F:htb_stock_data.csv')

# Creates the lists used in the calculation of the various parameters.
change, gain, loss, avggain, avgloss, rs, rsi, ema12, ema26, macdline, perck, bhs = [], [], [], [], [], [], [], [], [],\
                                                                                    [], [], []

# Adjusts the data from the CSV data file to the appropriate format.
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')

# Calculates the change in closing prices between following days.
# Zeros the first value in the CHANGE list.
change.append(0)

# Calculates the difference between today's and yesterday's closing price.
for i in range(len(df) - 1):
    change.append(df.loc[i + 1][4] - df.loc[i][4])

# From the CHANGE list determines the gain and zeros negative numbers.
for j in range(len(df)):
    if change[j] <= 0:
        gain.append(0)
    else:
        gain.append(change[j])

# From the CHANGES list determines the absolute negative values and zeros positive numbers.
for k in range(len(df)):
    if change[k] >= 0:
        loss.append(0)
    else:
        loss.append(-change[k])

# Calculates the smoothing constant for a 14 period RSI.
scrsi = 2 / (14 + 1)

# Creating the Average Gain value list.
# Zeros the first thirteen values in the list.
for m in range(13):
    avggain.append(0)

avggain.append(mean(gain[1:14]))
# Calculates the average gain using exponential moving averages.
for n in range(len(df) - 14):
    x = avggain[n + 13] + (gain[n + 14] - avggain[n + 13]) * scrsi
    avggain.append(x)

# Creating the Average Loss value list.
# Zeros the first thirteen values in the list.
for m in range(13):
    avgloss.append(0)

avgloss.append(mean(loss[1:14]))

# Calculates the average loss using exponential moving averages.
for n in range(len(df) - 14):
    x = avgloss[n + 13] + (loss[n + 14] - avgloss[n + 13]) * scrsi
    avgloss.append(x)

# Calculating the Relative Strength and appending to its list.
for o in range(len(df)):
    if avgloss[o] == 0:
        rs.append(0)
    else:
        rs.append(avggain[o] / avgloss[o])

# Calculating the Relative Strength Index and appending to the RSI list.
for q in range(len(df)):
    rsi.append(100 - (100 / (1 + rs[q])))

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
            bhs.append('HOLD')

# Create the Tensorflow database list.
dbtf = []

# Populate the TF DB.
for z in range(25, 35):
    dbtf.append([df.loc[z][4], df.loc[z][5], rsi[z], macdline[z], perck[z], bhs[z]])
