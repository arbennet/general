import yfinance as yf
import pandas as pd
from sys import argv

if __name__ == '__main__':
    script, Ticker, ReturnPeriod = argv

def ticker_hist (Ticker):
    """
    returns pandas dataframe containing yahoo finance history for given ticker
    """
    ticker = yf.Ticker(Ticker)
    df = ticker.history(period="max")
    df.insert(0, 'Ticker', Ticker)

    return df


def date_framing(df, window):
    """
    Filters dataframe for date window of interest
    """
    if window == 'Daily':
        pass
    elif window == 'Weekly':
        df = df.resample('W').last()
    elif window == 'BiWeekly':
        df = df.resample('W').last()
        df = df.loc[::2, :] # only every other
    elif window == 'Monthly':
        df = df.resample('M').last()
    elif window == 'Yearly':
        df = df.groupby([df.index.year]).tail(1)
    else:
        raise ValueError('Enter a valid return period (Weekly, BiWeekly, Monthly, Yearly).')
    
    df = df.sort_values(by='Date', ascending=False)
    df.insert(1, 'ReturnPeriod', window)

    return df


def attribution(df):
    """
    Returns performance attribution calcs
    """
    df['PrevClose'] = df['Close'].shift(-1)
    df['DeltaPrice'] = df['Close'] - df['PrevClose']
    df['Delta'] = df['DeltaPrice'] + df['Dividends']
    df['Return'] = df['Delta'] / df['PrevClose'] * 100

    return df


def returns(Ticker, ReturnPeriod):
    df = ticker_hist(Ticker)
    df = date_framing(df, ReturnPeriod)
    df = attribution(df)

    df = df.drop(columns=['Open','Volume','High','Low','Stock Splits','PrevClose'],axis=1)

    if __name__ == '__main__':
        return df 
    else:
        df.sort_index(inplace=True)
        return df

if __name__ == '__main__':
    print(returns(Ticker, ReturnPeriod).head(20))
