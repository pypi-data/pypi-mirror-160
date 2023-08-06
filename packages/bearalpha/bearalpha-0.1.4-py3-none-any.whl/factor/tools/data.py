import bearalpha as ba
import pandas as pd


@ba.Cache(prefix='factor_data', expire_time=259200)
def factor_data(factor, start: str, end: str, freq = ba.CBD):
    dates = pd.date_range(start=start, end=end, freq=freq)
    data = []
    with ba.PROGRESS as prog:
        for date in prog.track(dates):
            data.append(factor(date))
    data = pd.concat(data)
    return data.iloc[:, 0]

def group_mapping(start: str, end: str, freq = ba.CBD, source: str = 'citics'):
    stock = ba.Stock(ba.Cache().get('local'))
    dates = pd.date_range(start=start, end=end, freq=freq)
    data = []
    with ba.PROGRESS as prog:
        for date in prog.track(dates):
            data.append(stock.plate_info(start=date, end=date, 
                fields='first_industry_name', and_=f'source = "{source}"'))
    data = pd.concat(data)
    return data
    
def market_value(start: str, end: str, freq = ba.CBD):
    stock = ba.Stock(ba.Cache().get('local'))
    dates = pd.date_range(start=start, end=end, freq=freq)
    data = []
    with ba.PROGRESS as prog:
        for date in prog.track(dates):
            data.append(stock.derivative_indicator(start=date, end=date, fields='market_cap_2'))
    data = pd.concat(data)
    return data