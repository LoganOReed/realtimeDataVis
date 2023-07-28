import asyncio
from pprint import pprint
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from alpha_vantage.async_support.timeseries import TimeSeries

apiCall = True

# ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
symbols = [
    "GOOGL",
    "META",
    "ORCL",
    "MSFT",
    "ADBE",
]

async def getData(symbol):
    # ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
    ts = TimeSeries(key="G1ODTS0PTE9Q0JJC", output_format="pandas")
    data, _ = await ts.get_intraday(symbol,interval="1min")
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
    stockData ={"GOOGL": pd.read_csv("GOOGL_temp.csv")} 


if __name__ == "__main__":
    pprint(stockData)
    # plt.figure(figsize = (18,12))
    # plt.boxplot(stockData["GOOGL"][["open","high","low","close"]].transpose())
    # plt.show()
    sns.set_theme()
    sns.catplot(data=stockData["GOOGL"],
                x="time",
                y=["open","high","low","close"],
                # y="open",
                hue="volume",
                kind="box")
    # sns.relplot(
    #     data=stockData["GOOGL"],
    #     x="date", y="open", col="close",
    # )
    plt.show()
