import datetime
import os
import sys
import pandas as pd
import yahoo_fin.stock_info as si

os.chdir(sys.path[0])


#avec librairie yahoo_fin
quote_table = si.get_quote_table("aapl", dict_result=True)#dict_result=False to receive it as a pandas dataframe
print(quote_table)

#P/E ratio
pe_ratio = quote_table["PE Ratio (TTM)"]
print(f"P/E ratio: {pe_ratio}")

#autre maniere de faire, avec plusieurs tickers demandés en meme temps
dow_list = si.tickers_dow()

dow_stats = {}
for ticker in dow_list:
    temp = si.get_stats_valuation(ticker)
    temp = temp.iloc[:,:2]
    temp.columns = ["Attribute", "Recent"]
    dow_stats[ticker] = temp
print(dow_stats)

# to dataframe
combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()
print(combined_stats.head())

#cleaning
del combined_stats["level_1"]
# update column names
combined_stats.columns = ["Ticker", "Attribute", "Recent"]
print(combined_stats.head())