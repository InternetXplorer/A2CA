import os
import sys
import pandas as pd
import numpy as np


def get_financial_data(ticker_list):
    path = "../Bloomberg_data_processing/"
    filename = "preprocessed_sp500_data_01-02-22_with_sectors.csv"

    data = pd.read_csv(path + filename)

    companies_data = data.loc[data['Ticker'].isin(ticker_list)]
    companies_data = companies_data[["Ticker", "CUR_MKT_CAP", "CURR_ENTP_VAL", "EBIT", "EBITDA", "GROSS_PROFIT", "PE_RATIO"]].copy()
    print(companies_data)

    return companies_data


def compute_ratios(companies_data):
    companies_data["EV_EBIT_ratio"] = companies_data["CURR_ENTP_VAL"] / companies_data["EBIT"]
    companies_data["EV_EBITDA_ratio"] = companies_data["CURR_ENTP_VAL"] / companies_data["EBITDA"]
    # companies_data["EV_revenue_ratio"] = companies_data["CURR_ENTP_VAL"] / companies_data["revenue"]
    companies_data["EV_GROSS_PROFIT_ratio"] = companies_data["CURR_ENTP_VAL"] / companies_data["GROSS_PROFIT"]
    
    return companies_data