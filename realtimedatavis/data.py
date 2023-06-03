import asyncio
from pprint import pprint
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.async_support.timeseries import TimeSeries

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


loop = asyncio.get_event_loop()
tasks = [getData(symbol) for symbol in symbols]
group1 = asyncio.gather(*tasks)
results = loop.run_until_complete(group1)
loop.close()

stockData = pd.DataFrame(results)
stockData.columns = stockData.columns.str[3:]

# save to temp csv so I don't have to call the api as much
stockData.to_csv(index=False)


if __name__ == "__main__":
    pprint(stockData)

