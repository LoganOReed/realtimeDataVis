import asyncio
from pprint import pprint
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
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
    ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
    data, _ = await ts.get_intraday(symbol,interval="1min",outputsize="full")
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
        stockData[sym].to_csv(sym+"_temp.csv", index=False)
else:
    stockData = pd.read_csv("temp.csv")


if __name__ == "__main__":
    pprint(stockData)
    plt.figure(figsize = (18,12))
    plt.boxplot(stockData["GOOGL"][["open","high","low","close"]].transpose())
    plt.show()
