import finnhub
import pandas as pd
from time import time
from tqdm import tqdm


### ENUMS
API_KEY = 'bta0vr748v6rm8019cbg'
etf_dict = {"S&P":"SPY","NASDAQ":"QQQ","DOW":"DIA","RUSSELL":"VTWO"}
#########
finn_client = finnhub.Client(api_key=API_KEY)

def download_supported_stocks(market="US"):
    # Stock symbols
    all_us_symbols = finn_client.stock_symbols(market)
    return pd.DataFrame(all_us_symbols)

def download_candles(symbol,interval,start_epoch,end_epoch):
    res = finn_client.stock_candles(symbol, resolution=interval, _from=start_epoch, to=end_epoch)
    df = pd.DataFrame(res)
    df = df.drop('s',axis=1)
    df.columns = ['close',"high","low","open","timestamp","volume"]
    df['symbol'] = symbol
    return df


if __name__ == "__main__":
    ## If interested in seeing all of the stocks supported by the finnhub api, run the following
    # stocks = download_supported_stocks("US")
    # stocks.to_csv("data/Supported_API_Companies.xlsx")

    # ToDo: Create a file in config_files that keeps track of the high water mark for each of the stocks and only pull the latest data for each of the stocks
    # Pull all data (epoch of 0) for each of the desired symbols and save these to csv files
    start_time_epoch = 0
    curr_time_epoch = int(time())
    ## pull historic pricing data
    for (k,v) in etf_dict.items():
        df = download_candles(symbol=v,interval="D",start_epoch=start_time_epoch,end_epoch=curr_time_epoch)
        df.to_csv("data/{0}_{1}.csv".format(k,v),index=False)

