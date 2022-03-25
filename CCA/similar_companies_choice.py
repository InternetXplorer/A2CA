## !/usr/bin/env python
# coding: utf-8

# ### Imports
import pandas as pd
import numpy as np
import os
import sys

os.chdir(sys.path[0])


def process_data(companies_relevant_data):
    #standardization and applying log to some columns that need it. We get the data ready to be used to compare companies with each other
    companies_relevant_data["CUR_MKT_CAP"] = np.log(companies_relevant_data["CUR_MKT_CAP"])
    companies_relevant_data["CUR_MKT_CAP"] -= companies_relevant_data["CUR_MKT_CAP"].min()
    companies_relevant_data["CUR_MKT_CAP"] = companies_relevant_data["CUR_MKT_CAP"] / companies_relevant_data["CUR_MKT_CAP"].max()

    companies_relevant_data["NUM_OF_EMPLOYEES"] = np.log(companies_relevant_data["NUM_OF_EMPLOYEES"])
    companies_relevant_data["NUM_OF_EMPLOYEES"] -= companies_relevant_data["NUM_OF_EMPLOYEES"].min()
    companies_relevant_data["NUM_OF_EMPLOYEES"] = companies_relevant_data["NUM_OF_EMPLOYEES"] / companies_relevant_data["NUM_OF_EMPLOYEES"].max()

    if(companies_relevant_data["SUSTAIN_GROWTH_RT"].min()>0):
        companies_relevant_data["SUSTAIN_GROWTH_RT"] -= companies_relevant_data["SUSTAIN_GROWTH_RT"].min()
    else: # min wil become 0
        companies_relevant_data["SUSTAIN_GROWTH_RT"] += abs(companies_relevant_data["SUSTAIN_GROWTH_RT"].min())
    companies_relevant_data["SUSTAIN_GROWTH_RT"] = companies_relevant_data["SUSTAIN_GROWTH_RT"] / companies_relevant_data["SUSTAIN_GROWTH_RT"].max()
    return companies_relevant_data


def getData(standardize_data=True):
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
    companies_relevant_data = data[["Ticker", "IND_GICS", "SUB_IND_GICS", "CUR_MKT_CAP", "REGION_NAME", "NUM_OF_EMPLOYEES", "SUSTAIN_GROWTH_RT"]].copy() #headquarters location
    # companies_relevant_data.head()

    if(standardize_data):
        companies_relevant_data = process_data(companies_relevant_data)# standardization and/or applying log to some columns that need it. We get the data ready to be used to compare companies with each other
        print("Number of missing values per column in the dataset:\n")
        print(companies_relevant_data.isnull().sum())

    return companies_relevant_data


def get_similar_comp_ranking(studied_comp_ticker):
    # print("Ranking companies on similarity...")
    # ### Companies similarity ranking
    # Similarity will be determined based on sector, sub-industry, geography, and market cap (in this order of importance).


    companies_relevant_data = getData(standardize_data=True)
    # print("getData() result : ")
    # print(companies_relevant_data)

    # getting the studied company's data
    studied_comp_data = companies_relevant_data.loc[companies_relevant_data["Ticker"] == studied_comp_ticker].iloc[0]

    # next big step is computing distance between the studied company and every other company (we call it similarity score):

    # similarity_scores = pd.DataFrame(index=companies_relevant_data["Ticker"].copy())
    companies_data_with_similarity = getData(standardize_data=False) #dataframe where we will write the similarity results and that will be returned by function
    companies_data_with_similarity["similarity_score"] = 0.0
    # companies_relevant_data["similarity_score"] = 0.0

    # list of USA states
    # us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Washington DC', 
    # 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
    # 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
    # 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
    # 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    for index, row in companies_relevant_data.iterrows():
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
        temp = abs(row["CUR_MKT_CAP"] - studied_comp_data["CUR_MKT_CAP"])
        if(not np.isnan(temp)):
            similarity_score += temp
        else:
            similarity_score += 0.3

        # Add number of employees
        temp = abs(row["NUM_OF_EMPLOYEES"] - studied_comp_data["NUM_OF_EMPLOYEES"])
        if(not np.isnan(temp)):
            similarity_score += temp
        else:
            similarity_score += 0.3

        # Add growth rate
        temp = abs(row["SUSTAIN_GROWTH_RT"] - studied_comp_data["SUSTAIN_GROWTH_RT"])
        if(not np.isnan(temp)):
            similarity_score += temp

        # Add market geography
        if(row["REGION_NAME"] != studied_comp_data["REGION_NAME"]):
            similarity_score += 0.6

        # print(similarity_score)
        # companies_data_with_similarity["similarity_score"][row["Ticker"]] = similarity_score
        companies_data_with_similarity.loc[companies_data_with_similarity["Ticker"] == row["Ticker"], "similarity_score"] = similarity_score
        # companies_relevant_data["similarity_score"][row["Ticker"]] = similarity_score


    comp_data_sorted_by_similarity = companies_data_with_similarity.sort_values(by=["similarity_score"], ascending=True)
    comp_data_sorted_by_similarity = comp_data_sorted_by_similarity.set_index("Ticker")
    # sorted_similarity_scores = companies_relevant_data["similarity_score"].sort_values(ascending=True)
    # comp_data_sorted_by_similarity = comp_data_sorted_by_similarity.iloc[1:]

    # TODO : we could return additional info like MK_cap difference with studied comp, and booleans for each criteria (same sector, same sub-industry, same geography), for booleans, if false, provide the comp info
    # to provide more info to user about reasons these comps were chosen & make sure he's okay with this choice
    return comp_data_sorted_by_similarity


def statistical_analysis():
    companies_relevant_data = getData()
    print(companies_relevant_data.info())
    print(companies_relevant_data.describe())

# statistical_analysis()