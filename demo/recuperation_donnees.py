import os
import sys
import pandas as pd
import yahoo_fin.stock_info as si
import math

os.chdir(sys.path[0])


def get_financial_data(ticker_list):
    cached_data, remaining_tickers = get_from_cache(ticker_list)

    companies_data = {}
    for ticker in remaining_tickers:
        print(f"Recuperation de {ticker} sur yahoo finance")
        financial_data = {}
        
        statistics = si.get_stats_valuation(ticker)
        statistics = statistics.set_index(0)
        # statistics2 = si.get_stats(ticker)
        # print(statistics2)
        quarterly_income_statement_df = si.get_financials(ticker, yearly = False, quarterly = True)["quarterly_income_statement"]

        ev = statistics.loc["Enterprise Value 3"].tolist()[0]
        if(type(ev) == str):
            ev = float(ev[:-1])# pour enlever le 'B' à la fin du string (indique que le chiffre est en milliard, il faudra faire attention que l'unité soit la meme partout)
        financial_data["EV"] = ev*(10**3)
        
        financial_data["EBIT"] = quarterly_income_statement_df.loc["ebit"][0]/(10**6)# [0] pour date la plus recente

        financial_data["revenue"] = quarterly_income_statement_df.loc["totalRevenue"][0]/(10**6)

        financial_data["gross_profit"] = quarterly_income_statement_df.loc["grossProfit"][0]/(10**6)

        companies_data[ticker] = financial_data
    
    companies_data = pd.DataFrame.from_dict(companies_data, orient='index')
    companies_data = pd.concat([cached_data, companies_data])
    save_to_disk(companies_data)
    return companies_data


def save_to_disk(companies_data):
    companies_data = companies_data.reset_index()
    companies_data.rename(columns={'index':'ticker'}, inplace=True)
    if(not os.path.exists("cache/")):
        os.mkdir("cache")
    elif (os.path.isfile("cache/companies_data.csv")):
        saved_data = pd.read_csv("cache/companies_data.csv")
        companies_data = pd.concat([companies_data, saved_data]).drop_duplicates()
    
    companies_data.to_csv("cache/companies_data.csv", index=False)

def get_from_cache(ticker_list, allow_nan=False):
    saved_data = None
    remaining_tickers = ticker_list.copy()
    if (os.path.isfile("cache/companies_data.csv")):
        saved_data = pd.read_csv("cache/companies_data.csv")
        saved_data = saved_data[saved_data['ticker'].isin(ticker_list)]
        if(not allow_nan):
            saved_data.dropna(axis='rows', inplace=True)
        
        saved_data_tickers = saved_data["ticker"].tolist()
        remaining_tickers = [ticker for ticker in ticker_list if ticker not in saved_data_tickers]
        saved_data.set_index("ticker", inplace = True)
    return saved_data, remaining_tickers


def calcul_ratios(companies_data):
    companies_data["EV_EBIT_ratio"] = companies_data["EV"] / companies_data["EBIT"]
    companies_data["EV_revenue_ratio"] = companies_data["EV"] / companies_data["revenue"]
    companies_data["EV_gross_profit_ratio"] = companies_data["EV"] / companies_data["gross_profit"]
    
    return companies_data


ticker_list = ['F', 'VWAGY', 'SZKMY', 'FB']
df = get_financial_data(ticker_list)
print(df)

# ticker_list = ['F', 'VWAGY', 'SZKMY', 'FB']
# data, remaining_tickers = get_from_cache(ticker_list)
# print(data)
# print(remaining_tickers)