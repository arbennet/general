import yfinance as yf
import pandas as pd
import datetime
from sys import argv

script, Ticker, ReturnPeriod = argv

def ticker_hist (Ticker):
    """
    returns pandas dataframe containing yahoo finance history for given ticker
    """
    ticker = yf.Ticker(Ticker)
    df = ticker.history(period="max")
    df.insert(0, 'Ticker', Ticker)

    return df


def derive_columns(df):
    """
    derives columns needed for performance attribution
    """
    df['DateTime'] = pd.to_datetime(df.index)
    df['day_of_week'] = df['DateTime'].dt.day_name()
    df['DivCumSum'] = df.Dividends.cumsum()

    return df


def date_framing(df, window):
    """
    Filters dataframe for date ranges of interest
    """
    if window == 'Weekly':
        df = df.sort_values(by='Date', ascending=False)
        max_weekday = df['day_of_week'].iloc[0]
        df = df[df.day_of_week == max_weekday]
    elif window == 'BiWeekly':
        df = df.sort_values(by='Date', ascending=False)
        max_weekday = df['day_of_week'].iloc[0]
        df = df[df.day_of_week == max_weekday]
        df = df.loc[::2, :] # only get paid every other Thursday
    elif window == 'Monthly':
        df = df.groupby([df.index.year, df.index.month]).tail(1)
        df = df.sort_values(by='Date', ascending=False)
    elif window == 'Yearly':
        df = df.groupby([df.index.year]).tail(1)
        df = df.sort_values(by='Date', ascending=False)
    else:
        raise ValueError('Enter a valid return period.')

    df.insert(1, 'ReturnPeriod', window)

    return df


def attribution_cols (df):
    """
    Returns performance attribution calcs
    """
    df['PrevClose'] = df['Close'].shift(-1)
    df['DeltaDividend'] = df['DivCumSum'] - df['DivCumSum'].shift(-1)
    df['DeltaPrice'] = df['Close'] - df['PrevClose']
    df['Delta'] = df['DeltaPrice'] + df['DeltaDividend']
    df['Return'] = df['Delta'] / df['PrevClose'] * 100

    return df


def main(Ticker, ReturnPeriod):
    df = ticker_hist(Ticker)
    df = derive_columns(df)
    df = date_framing(df, ReturnPeriod)
    df = attribution_cols(df)

    df = df.drop(columns=['Open','Volume','High','Low','day_of_week','Dividends', 'Stock Splits', 'DateTime', 'DivCumSum'])

    return print(df.head(20))

main(Ticker, ReturnPeriod)
