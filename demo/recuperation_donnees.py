import os
import sys
import pandas as pd
import yahoo_fin.stock_info as si
import math

os.chdir(sys.path[0])


def get_financial_data(ticker_list):
    companies_data = {}
    for ticker in ticker_list:
        financial_data = {}

        statistics = si.get_stats_valuation(ticker)
        statistics = statistics.set_index(0)
        # statistics2 = si.get_stats(ticker)
        # print(statistics2)
        quarterly_income_statement_df = si.get_financials(ticker, yearly = False, quarterly = True)["quarterly_income_statement"]

        ev = statistics.loc["Enterprise Value 3"].tolist()[0]
        if(type(ev) == str):
            ev = float(ev[:-1])# pour enlever le 'B' à la fin du string (indique que le chiffre est en milliard, il faudra faire attention que l'unité soit la meme partout)
        financial_data["EV"] = ev#*(10**9)
        
        financial_data["EBIT"] = quarterly_income_statement_df.loc["ebit"][0]# [0] pour date la plus recente

        financial_data["revenue"] = quarterly_income_statement_df.loc["totalRevenue"][0]

        financial_data["gross_profit"] = quarterly_income_statement_df.loc["grossProfit"][0]

        companies_data[ticker] = financial_data

    return pd.DataFrame.from_dict(companies_data, orient='index')

# ticker_list = ['F', 'VWAGY', 'SZKMY', 'NSANY', 'HMC', 'TM', 'STLA']
# df = get_financial_data(ticker_list)
# print(df.info())
# print(df)