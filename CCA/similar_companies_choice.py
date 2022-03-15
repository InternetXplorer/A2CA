#!/usr/bin/env python
# coding: utf-8

# ### Imports
import pandas as pd
import numpy as np


def getData():
    # ### Data loading and preprocessing

    path = "../Bloomberg_data_processing/"
    filename = "preprocessed_russell_3k_data_14-03-22.csv"

    data = pd.read_csv(path + filename)
    # print(data.head(2))


    # ### GICS sectors & sub-industry data exploration
    # data['GICS Sector'].nunique()
    # data.groupby(['GICS Sector'])["GICS Sector"].count()
    # data["GICS Sub-Industry"].nunique()
    # data["GICS Sub-Industry"].describe()
    # pd.DataFrame(data.groupby(['GICS Sector', 'GICS Sub-Industry'])["GICS Sub-Industry"].count()).head(15)


    # dataset with only usefull columns
    companies_relevant_info = data[["Ticker", "IND_GICS", "SUB_IND_GICS", "CUR_MKT_CAP", "NUM_OF_EMPLOYEES", "SUSTAIN_GROWTH_RT"]].copy() #headquarters location
    companies_relevant_info.head()

    companies_relevant_info["CUR_MKT_CAP"] = np.log(companies_relevant_info["CUR_MKT_CAP"])
    companies_relevant_info["CUR_MKT_CAP"] -= companies_relevant_info["CUR_MKT_CAP"].min()
    companies_relevant_info["CUR_MKT_CAP"] = companies_relevant_info["CUR_MKT_CAP"] / companies_relevant_info["CUR_MKT_CAP"].max()

    companies_relevant_info["NUM_OF_EMPLOYEES"] = np.log(companies_relevant_info["NUM_OF_EMPLOYEES"])
    companies_relevant_info["NUM_OF_EMPLOYEES"] -= companies_relevant_info["NUM_OF_EMPLOYEES"].min()
    companies_relevant_info["NUM_OF_EMPLOYEES"] = companies_relevant_info["NUM_OF_EMPLOYEES"] / companies_relevant_info["NUM_OF_EMPLOYEES"].max()

    if(companies_relevant_info["SUSTAIN_GROWTH_RT"].min()>0):
        companies_relevant_info["SUSTAIN_GROWTH_RT"] -= companies_relevant_info["SUSTAIN_GROWTH_RT"].min()
    else: # min wil become 0
        companies_relevant_info["SUSTAIN_GROWTH_RT"] += abs(companies_relevant_info["SUSTAIN_GROWTH_RT"].min())
    companies_relevant_info["SUSTAIN_GROWTH_RT"] = companies_relevant_info["SUSTAIN_GROWTH_RT"] / companies_relevant_info["SUSTAIN_GROWTH_RT"].max()


    print("Number of missing values per column in the dataset:\n")
    print(companies_relevant_info.isnull().sum())
    return companies_relevant_info


def get_similar_comp_ranking(studied_comp_ticker):
    # print("Ranking companies on similarity...")
    # ### Companies similarity ranking
    # Similarity will be determined based on sector, sub-industry, geography, and market cap (in this order of importance).

    # API à tester pour récupérer le nom du pays à partir de la 'Headquarters location' :
    # https://apilayer.com/marketplace/description/geo-api#pricing

    companies_relevant_info = getData()

    # getting the studied company's data
    # studied_comp_ticker = "MMM"
    studied_comp_data = companies_relevant_info.loc[companies_relevant_info["Ticker"] == studied_comp_ticker].iloc[0]
    # studied_comp_data

    # computing distance between the studied company and every other company
    # similarity_scores = []
    similarity_scores = pd.DataFrame(index=companies_relevant_info["Ticker"].copy())
    similarity_scores["similarity_score"] = 0.0

    # list of USA states
    us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Washington DC', 
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
    'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    for index, row in companies_relevant_info.iterrows():
        similarity_score = 0 # lowest = most similar

        # Checking industry and sub industry similarity
        if(row["IND_GICS"] != studied_comp_data["IND_GICS"]):
            similarity_score += 10 # biggest penalty, sector is the most important thing the companies need to have in common
        elif(row["SUB_IND_GICS"] != studied_comp_data["SUB_IND_GICS"]):
            similarity_score += 1

        # Checking location similarity
        # if((row["Headquarters Location"].split(sep=',')[1]) in us_states and (studied_comp_data["Headquarters Location"].split(sep=',')[1]) in us_states): # checking if the companies are both located in the US
        #     if(row["Headquarters Location"].split(sep=',')[0]!=studied_comp_data["Headquarters Location"].split(sep=',')[0]): # checking if the companies are both located in the same US state
        #         similarity_score += 0.3
        # elif((row["Headquarters Location"].split(sep=',')[1])!=studied_comp_data["Headquarters Location"].split(sep=',')[1]): # checking if the companies are both located in the same country
        #     similarity_score += 0.6

        # Add market cap difference
        similarity_score += abs(row["CUR_MKT_CAP"] - studied_comp_data["CUR_MKT_CAP"])

        # Add number of employees 
        similarity_score += abs(row["NUM_OF_EMPLOYEES"] - studied_comp_data["NUM_OF_EMPLOYEES"])

        # Add growth rate 
        similarity_score += abs(row["SUSTAIN_GROWTH_RT"] - studied_comp_data["SUSTAIN_GROWTH_RT"])

        # Add market geography
        # No market geography found on Bloomberg terminal


        # and if one info is missing (market cap mostly) either leave as NaN (will be considered lowest similarity and that company will never be used) or, if we want to use that company nevertheless, give penalty of either max or average difference for that info (for example max diff for mk cap is 1 and avg is 0.288228)

        similarity_scores["similarity_score"][row["Ticker"]] = similarity_score

    sorted_similarity_scores = similarity_scores["similarity_score"].sort_values(ascending=True)
    sorted_similarity_scores = sorted_similarity_scores.iloc[1:]
    # print(sorted_similarity_scores.head(10))

    # TODO : we could return additional info like MK_cap difference with studied comp, and booleans for each criteria (same sector, same sub-industry, same geography), for booleans, if false, provide the comp info
    # to provide more info to user about reasons these comps were chosen & make sure he's okay with this choice
    return sorted_similarity_scores