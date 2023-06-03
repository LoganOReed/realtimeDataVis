import asyncio
from pprint import pprint
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.async_support.timeseries import TimeSeries

apiCall = False

# ts = TimeSeries(key="R0AU0EWLEJEKDL6W", output_format="pandas")
symbols = [
    "GOOGL",
    "META",
    "ORCL",
    "MSFT",
    "ADBE",
]

async def getData(symbol):
    ts = TimeSeries(key="R0AU0EWLEJEKDL6W")
    data, _ = await ts.get_quote_endpoint(symbol)
    await ts.close()
    return data

if apiCall:
    loop = asyncio.get_event_loop()
    tasks = [getData(symbol) for symbol in symbols]
    group1 = asyncio.gather(*tasks)
    results = loop.run_until_complete(group1)
    loop.close()

    stockData = pd.DataFrame(results)
    stockData.columns = stockData.columns.str[3:]
    stockData.to_csv("temp.csv", index=False)
else:
    stockData = pd.read_csv("temp.csv")



if __name__ == "__main__":
    pprint(stockData)

