import os
import sys
import pandas as pd
import random
from recuperation_donnees import get_financial_data

os.chdir(sys.path[0])


# Récupération des données
ticker_list = ['F', 'SZKMY', 'NSANY', 'HMC', 'TM', 'STLA'] #secteur de l'automobile (sans respecter de proximité geographique)
# ticker_list = ['F']
num_of_comparable_companies = len(ticker_list) - 1
# num_of_comparable_companies = 5
studied_comp_ticker = "F"
companies_data = get_financial_data(ticker_list)
nbr_of_na = companies_data.isna().sum().sum()
if (nbr_of_na > 0):
    print(f"{nbr_of_na} missing values. Rows with NaN will be dropped.")
    companies_data = companies_data.dropna(axis='rows')
# print(companies_data.info())
# print(companies_data)

# companies_data = {}
# for i in range(0, num_of_comparable_companies+1):
#     financial_data = {}
#     financial_data["EV"] = random.randint(10, 50)
#     financial_data["EBITDA"] = random.randint(1, 12)
#     financial_data["EBIT"] = random.randint(1, 10)
#     financial_data["revenue"] = random.randint(1, 50)
#     financial_data["gross_profit"] = random.randint(3, 20)
#     financial_data["P_E_ratio"] = random.randint(1, 15)
#     company_name = ""
#     if(i == 0):
#         company_name = studied_comp_name
#     else:
#         company_name = "company_" + str(i)

#     companies_data[company_name] = financial_data



#Calcul des ratios
# for comp_name in companies_data.keys():
#     # companies_data[comp_name]["EV_EBITDA_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBITDA"]
#     companies_data[comp_name]["EV_EBIT_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBIT"]
#     companies_data[comp_name]["EV_revenue_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["revenue"]
#     companies_data[comp_name]["EV_gross_profit_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["gross_profit"]
companies_data["EV_EBIT_ratio"] = companies_data["EV"] / companies_data["EBIT"]
companies_data["EV_revenue_ratio"] = companies_data["EV"] / companies_data["revenue"]
companies_data["EV_gross_profit_ratio"] = companies_data["EV"] / companies_data["gross_profit"]

print(companies_data)


#calcul des moyennes
# averages = {}

# averages["EV_EBITDA_ratio"] = 0
# averages["EV_EBIT_ratio"] = 0
# averages["EV_revenue_ratio"] = 0
# averages["EV_gross_profit_ratio"] = 0
# averages["P_E_ratio"] = 0

# for comp_name in companies_data.keys():
#     if(comp_name != studied_comp_name):
#         # averages["EV_EBITDA_ratio"] += companies_data[comp_name]["EV_EBITDA_ratio"]
#         averages["EV_EBIT_ratio"] += companies_data[comp_name]["EV_EBIT_ratio"]
#         averages["EV_revenue_ratio"] += companies_data[comp_name]["EV_revenue_ratio"]
#         averages["EV_gross_profit_ratio"] += companies_data[comp_name]["EV_gross_profit_ratio"]
#         averages["P_E_ratio"] += companies_data[comp_name]["P_E_ratio"]

# # averages["EV_EBITDA_ratio"] /= num_of_comparable_companies
# averages["EV_EBIT_ratio"] /= num_of_comparable_companies
# averages["EV_revenue_ratio"] /= num_of_comparable_companies
# averages["EV_gross_profit_ratio"] /= num_of_comparable_companies
# averages["P_E_ratio"] /= num_of_comparable_companies

print("\naverages :")
averages = companies_data.mean(axis=0)
print(averages)





#estimation d'EV de l'entreprise étudiée a partir du ratio EV / EBIT
ratio_to_be_used = "EV_EBIT_ratio"
denominator_stat = "EBIT"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print("\n\n(EVs are in billion of dollars.)\n")
print(f"Real EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")



ratio_to_be_used = "EV_revenue_ratio"
denominator_stat = "revenue"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print(f"\nReal EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")


ratio_to_be_used = "EV_gross_profit_ratio"
denominator_stat = "gross_profit"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print(f"\nReal EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")