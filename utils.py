import datetime as dt
import pandas as pd


def get_last_7_days():

    today = dt.datetime.now()
    weekday = today.weekday()
    end = today  # will change if we are looking today's market after closing time
    if weekday == 6:
        days = 11
    elif weekday == 5:
        days = 10
    else:
        if today.hour >= 16:  # when market is closed today
            end = today + dt.timedelta(days=1)
            if weekday == 0:  # monday
                days = 11  # days to subtract to get last 8 active trading days data
            else:  # for all others day
                days = 9  # days to subtract will be just 9 including today
        else:
            if weekday == 0 or weekday == 1:  # monday or tuesday
                days = 12  # days to subtract to get last 8 active trading days data
            else:  # for all others day
                days = 10  # days to subtract will be just 10 excluding today
        # if got confused in future just check calender
        # basically we are taking last 8 trading days including today if 4 pm is over
        # so later so today's day will be used to compare range with previous 7 days
        # if 4 pm is not over then yesterday's day will considered to compare with yesterday's previous 7 days

    DD = dt.timedelta(days=days)
    start = today - DD
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    return start, end


def get_range(df):
    df = df.copy()
    df['Range'] = abs(df['High'] - df['Low'])
    return df
