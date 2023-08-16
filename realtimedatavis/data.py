import asyncio
from pprint import pprint
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime as datetime
import seaborn as sns
from alpha_vantage.async_support.timeseries import TimeSeries

apiCall = True

# ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
symbols = [
    "GOOGL",
    "META",
    "MSFT",
]


async def getData(symbol):
    # ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
    ts = TimeSeries(key="G1ODTS0PTE9Q0JJC", output_format="pandas")
    data, _ = await ts.get_intraday(symbol, interval="1min")
    await ts.close()
    return data

if apiCall:
    loop = asyncio.get_event_loop()
    tasks = [getData(symbol) for symbol in symbols]
    group1 = asyncio.gather(*tasks)
    results = loop.run_until_complete(group1)
    loop.close()
    stockData = dict(zip(symbols, results))

    for sym in symbols:
        stockData[sym].columns = stockData[sym].columns.str[3:]
        stockData[sym]["time"] = stockData[sym].index.to_list()
        stockData[sym].to_csv(sym+"_temp.csv", index=True)

else:
    stockData = {
            "GOOGL": pd.read_csv("GOOGL_temp.csv",index_col=0,parse_dates=True),
            "META": pd.read_csv("META_temp.csv",index_col=0,parse_dates=True),
            "ORCL": pd.read_csv("ORCL_temp.csv",index_col=0,parse_dates=True),
            "MSFT": pd.read_csv("MSFT_temp.csv",index_col=0,parse_dates=True),
            "ADBE": pd.read_csv("ADBE_temp.csv",index_col=0,parse_dates=True)
            }



if __name__ == "__main__":
    pprint(stockData)
    print(stockData["GOOGL"][["time"]])
    # sns.set_theme()
    # plt.figure(figsize=(18, 12))
    # plt.boxplot(stockData["GOOGL"][["open", "high", "low", "close"]].transpose())
    # plt.show()
    # sns.catplot(data=stockData["GOOGL"][["date", "open", "high", "low", "close"]], kind="box")

    # fig, axs = plt.subplots(ncols=4, nrows=2, figsize=(5.5,3.5), layout="constrained")
    # # add an artist, in this case a nice label in the middle...
    # for row in range(2):
    #     for col in range(2):
    #         axs[row, col].annotate(f'axs[{row}, {col}]', (0.5, 0.5),
    #                                transform=axs[row, col].transAxes,
    #                                ha='center', va='center', fontsize=18,
    #                                color='darkgrey')
    # axs[0, 0].plot(pd.to_datetime(stockData["GOOGL"]["time"]), stockData["GOOGL"]["open"])
    # axs[0, 0].plot(pd.to_datetime(stockData["GOOGL"]["time"]), stockData["GOOGL"]["volume"])
    # axs[0, 2].plot(pd.to_datetime(stockData["GOOGL"]["time"]), stockData["GOOGL"]["high"])
    # axs[0, 3].plot(pd.to_datetime(stockData["GOOGL"]["time"]), stockData["GOOGL"]["low"])
    # fig.suptitle('GOOGL')
    # plt.show()
    fig = mpf.figure(figsize=(9,6), style="starsandstripes")
    ax1 = fig.add_subplot(2,3,1)
    ax2 = fig.add_subplot(2,3,2)
    ax3 = fig.add_subplot(2,3,3)
    av1 = fig.add_subplot(3,3,7,sharex=ax1)
    av2 = fig.add_subplot(3,3,8,sharex=ax1)
    av3 = fig.add_subplot(3,3,9,sharex=ax3)

    mpf.plot(stockData["GOOGL"].sort_index(ascending=True), ax=ax1, volume=av1, type="candle", mav=(3,9,15), xrotation=15, axtitle="GOOGL")
    mpf.plot(stockData["META"].sort_index(ascending=True), ax=ax2, volume=av2, type="candle", mav=(3,9,15), xrotation=15, axtitle="META")
    mpf.plot(stockData["MSFT"].sort_index(ascending=True), ax=ax3, volume=av3, type="candle", mav=(3,9,15), xrotation=15, axtitle="MSFT")
    plt.show()

