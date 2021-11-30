import os
import sys
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from recuperation_donnees import get_financial_data
from recuperation_donnees import calcul_ratios
from sklearn.linear_model import LinearRegression

os.chdir(sys.path[0])


# Récupération des données
ticker_list = ['F', 'SZKMY', 'NSANY', 'HMC', 'TM', 'STLA', 'BMW.DE'] #secteur de l'automobile (sans respecter de proximité geographique)
ticker_european_car_manuf = ['STLA', 'BMW.DE', 'VOW.DE', 'RNO.PA', 'VOLV-A.ST']
ticker_list = ticker_european_car_manuf
num_of_comparable_companies = len(ticker_list) - 1
studied_comp_ticker = "STLA"

companies_data = get_financial_data(ticker_list)

nbr_of_na = companies_data.isna().sum().sum()
if (nbr_of_na > 0):
    print(f"{nbr_of_na} missing values. Rows with NaN will be dropped.")
    companies_data = companies_data.dropna(axis='rows')
# print(companies_data.info())
# print(companies_data)

companies_data = calcul_ratios(companies_data)
print(companies_data)


#Scatter plot
stat = "EBIT"
ax = companies_data.plot.scatter(stat, "EV", title=f"Scatter plot of EV and {stat}")

# Annotate each data point
for i, txt in enumerate(companies_data.index):
   ax.annotate(txt, (companies_data[stat].iat[i]+0.05, companies_data["EV"].iat[i]))



#calcul des moyennes
print("\nAverages :")
averages = companies_data.mean(axis=0)
print(averages)

#estimation d'EV de l'entreprise étudiée a partir du ratio EV / EBIT
ratio_to_be_used = "EV_EBIT_ratio"
denominator_stat = "EBIT"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print("\n\n(Values are in millions of dollars.)\n")
print(f"Real EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")

#estimation d'EV de l'entreprise étudiée a partir du ratio EV / revenue
ratio_to_be_used = "EV_revenue_ratio"
denominator_stat = "revenue"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print(f"\nReal EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")

#estimation d'EV de l'entreprise étudiée a partir du ratio EV / gross_profit
ratio_to_be_used = "EV_gross_profit_ratio"
denominator_stat = "gross_profit"
estimated_EV = averages.loc[ratio_to_be_used] * companies_data.loc[studied_comp_ticker, denominator_stat]

print(f"\nReal EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} (using avg {ratio_to_be_used}): {estimated_EV} ")
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}")




# Estimation using linear regression
stat_used = "gross_profit"
ax = companies_data.plot.scatter(stat_used, "EV", title=f"Scatter plot of EV and {stat_used}")

# Annotate each data point
for i, txt in enumerate(companies_data.index):
   ax.annotate(txt, (companies_data[stat_used].iat[i]+0.05, companies_data["EV"].iat[i]))



X_single_var = companies_data[companies_data.index != studied_comp_ticker][[stat_used]].reset_index(drop=True) #single variable
# X_multi_var = companies_data[companies_data.index != studied_comp_ticker][["EBIT", "revenue", "gross_profit"]].reset_index(drop=True) #multi variable
Y = companies_data[companies_data.index != studied_comp_ticker]["EV"].reset_index(drop=True)
studied_comp_row_single_var = companies_data[companies_data.index == studied_comp_ticker][[stat_used]].reset_index(drop=True) #single variable
# studied_comp_row_multi_var = companies_data[companies_data.index == studied_comp_ticker][["EBIT", "revenue", "gross_profit"]].reset_index(drop=True) #multi variable

linear_regressor = LinearRegression()
linear_regressor.fit(X_single_var, Y) #single variable
# linear_regressor.fit(X_multi_var, Y) #multi variable
print(f"\nCoefs ligne de regression :\na={round(linear_regressor.coef_[0], 4)}\nintercept={round(linear_regressor.intercept_, 4)}\n") #single variable
# print(f"\n\nCoefs ligne de regression :\ncoefs={linear_regressor.coef_, 4}\nnintercept={round(linear_regressor.intercept_, 4)}\n") #multi variable
estimated_EV = linear_regressor.predict(studied_comp_row_single_var)[0] #single variable
# estimated_EV = linear_regressor.predict(studied_comp_row_multi_var)[0] #multi variable

print(f"Real EV of {studied_comp_ticker}: {companies_data.loc[studied_comp_ticker, 'EV']}")
print(f"Estimated EV of {studied_comp_ticker} with regression model (using {stat_used}): {estimated_EV} ") #single variable
# print(f"Estimated EV of {studied_comp_ticker} with regression model (using all stats): {estimated_EV} ") #multi variable
print(f"real EV / Estimated EV : {companies_data.loc[studied_comp_ticker, 'EV'] / estimated_EV}\n")

plt.plot(X_single_var, X_single_var*linear_regressor.coef_ + linear_regressor.intercept_, color='red') #single variable
plt.show()