import os
import sys
import pandas as pd
import random

os.chdir(sys.path[0])


# Récupération des données
# on imagine qu'on récupère ces données réellement, via API ou webscapping
num_of_comparable_companies = 5
companies_data = {}

for i in range(0, num_of_comparable_companies+1):
    financial_data = {}
    financial_data["EV"] = random.randint(1, 50)
    financial_data["EBITDA"] = random.randint(1, 50)
    financial_data["EBIT"] = random.randint(1, 50)
    financial_data["revenue"] = random.randint(1, 50)
    financial_data["gross_profit"] = random.randint(1, 50)
    financial_data["P_E_ratio"] = random.randint(1, 50)
    company_name = ""
    if(i == 0):
        company_name = "studied_company"
    else:
        company_name = "company_" + str(i)

    companies_data[company_name] = financial_data



#Calcul des ratios
for comp_name in companies_data.keys:
    companies_data[comp_name]["EV_EBITDA_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBITDA"]
    companies_data[comp_name]["EV_EBIT_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBIT"]
    companies_data[comp_name]["EV_revenue_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["revenue"]
    companies_data[comp_name]["EV_gross_profit_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["gross_profit"]


#calcul des moyennes
averages = {}

