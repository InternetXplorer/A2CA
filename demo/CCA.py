import os
import sys
import pandas as pd
import random

os.chdir(sys.path[0])


# Récupération des données
# on imagine qu'on récupère ces données réellement, via API ou webscapping
num_of_comparable_companies = 5
studied_comp_name = "studied_company"
companies_data = {}

for i in range(0, num_of_comparable_companies+1):
    financial_data = {}
    financial_data["EV"] = random.randint(10, 50)
    financial_data["EBITDA"] = random.randint(1, 12)
    financial_data["EBIT"] = random.randint(1, 10)
    financial_data["revenue"] = random.randint(1, 50)
    financial_data["gross_profit"] = random.randint(3, 20)
    financial_data["P_E_ratio"] = random.randint(1, 15)
    company_name = ""
    if(i == 0):
        company_name = studied_comp_name
    else:
        company_name = "company_" + str(i)

    companies_data[company_name] = financial_data



#Calcul des ratios
for comp_name in companies_data.keys():
    companies_data[comp_name]["EV_EBITDA_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBITDA"]
    companies_data[comp_name]["EV_EBIT_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["EBIT"]
    companies_data[comp_name]["EV_revenue_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["revenue"]
    companies_data[comp_name]["EV_gross_profit_ratio"] = companies_data[comp_name]["EV"] / companies_data[comp_name]["gross_profit"]


#calcul des moyennes
averages = {}

averages["EV_EBITDA_ratio"] = 0
averages["EV_EBIT_ratio"] = 0
averages["EV_revenue_ratio"] = 0
averages["EV_gross_profit_ratio"] = 0
averages["P_E_ratio"] = 0

for comp_name in companies_data.keys():
    if(comp_name != studied_comp_name):
        averages["EV_EBITDA_ratio"] += companies_data[comp_name]["EV_EBITDA_ratio"]
        averages["EV_EBIT_ratio"] += companies_data[comp_name]["EV_EBIT_ratio"]
        averages["EV_revenue_ratio"] += companies_data[comp_name]["EV_revenue_ratio"]
        averages["EV_gross_profit_ratio"] += companies_data[comp_name]["EV_gross_profit_ratio"]
        averages["P_E_ratio"] += companies_data[comp_name]["P_E_ratio"]

averages["EV_EBITDA_ratio"] /= num_of_comparable_companies
averages["EV_EBIT_ratio"] /= num_of_comparable_companies
averages["EV_revenue_ratio"] /= num_of_comparable_companies
averages["EV_gross_profit_ratio"] /= num_of_comparable_companies
averages["P_E_ratio"] /= num_of_comparable_companies

print(averages)

#estimation d'EV de l'entreprise étudiée
estimated_EV = averages["EV_EBITDA_ratio"] * companies_data[studied_comp_name]["EV_EBITDA_ratio"]

print(f"Real EV : {companies_data[studied_comp_name]['EV']}")
print(f"Estimated EV : {estimated_EV}")