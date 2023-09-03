# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import seaborn
import pandas as pd
import numpy as np
import os
import datetime
from country_converter import CountryConverter

# Set your path to the project folder
path = "/files/Data/"
os.chdir(path)

smoking_orig = pd.read_csv("smoking.csv")
#print(smoking_orig.head(5))
gdp_orig = pd.read_csv("GDP.csv", header=2)
#print(gdp_orig.head(5))

###############################
###  Data Cleaning & Merging ##
###############################

# Drop unnamed column at the end with nan
gdp_orig = gdp_orig.drop(['Unnamed: 67'], axis=1)
# Change to long format
# Only take the years from the columns
years=list(gdp_orig.columns[4:])

# Use pd.melt to unpivot all the year columns
# ID variable as Country Name & Country Code
# Value_vars is Years (all columns are from 1960-2022 with the value_name GDPpC
gdp_long = pd.melt(gdp_orig,id_vars=['Country Name','Country Code'],\
value_vars=years, var_name='Year', value_name='GDPpC', ignore_index=False)
# Check for right type
gdp_long.dtypes
smoking_orig.dtypes
# Year is a str object and not an integer
gdp_long["Year"] = pd.to_numeric(gdp_long["Year"])
gdp_long = gdp_long.convert_dtypes()
smoking = smoking_orig.convert_dtypes()
# Check if it worked: Yes!
print(gdp_long.dtypes)
print(smoking.dtypes)
# Drop all years before 1980 (smoking.csv starts at 1980)
gdp_long = gdp_long[gdp_long['Year'] >= 1980]

# Merge smoking and gdp_long
# Join on Country names and check if they are equal or not
combined_df = gdp_long.merge(smoking, \
left_on=["Country Name","Year"], right_on=["Country","Year"], how="left")
# Drop all rows with no matching Country = Country Name pairs
gdp_smoking = combined_df[combined_df.Country != 0]
gdp_smoking = gdp_smoking.drop(['Country Code','Country' ], axis=1)
gdp_smoking.dtypes
# Turn Year int column to datetime format
gdp_smoking["Year"] = pd.to_datetime(gdp_smoking.Year, format='%Y')

# 458 missing values for GDPpC
nan_count_total = gdp_smoking.isna().sum()
print(nan_count_total)
# Count the number of NaN values in "GDPpC" column for each country
nan_count_country = gdp_smoking.groupby('Country Name')['GDPpC'].apply(lambda x: x.isna().sum()).reset_index()
# Rename the column for clarity
nan_count_country.columns = ['Country Name', 'NaN Count']
nan_count_country = nan_count_country.sort_values(['Country Name', 'NaN Count'], ascending = [True, True])

# Define a threshold (in this case, 4) for NaN counts
threshold = 4
# Filter the DataFrame to keep only countries with NaN counts less than or equal to the threshold
filtered_df = gdp_smoking[gdp_smoking['Country Name'].isin(nan_count_country[nan_count_country['NaN Count'] <= threshold]['Country Name'])]
nan_count_country = filtered_df.groupby('Country Name')['GDPpC'].apply(lambda x: x.isna().sum()).reset_index()
print(nan_count_country)

filtered_df = filtered_df.sort_values(['Country Name', 'Year'], ascending = [True, True])
filtered_df = filtered_df.reset_index().drop(["index"], axis=1)
# Backfill NaN values in "GDPpC" column within each country
filtered_df['GDPpC'] = filtered_df.groupby('Country Name')['GDPpC'].fillna(method='backfill')
# Rename the columns

filtered_df = filtered_df.rename(columns={
    'Data.Daily cigarettes': 'Daily Cigarette Consumption',
    'Data.Percentage.Male': 'Percentage of Male Smokers',
    'Data.Percentage.Female': 'Percentage of Female Smokers',
    'Data.Percentage.Total': 'Percentage of Total Smokers',
    'Data.Smokers.Total': 'Total Number of Smokers',
    'Data.Smokers.Female': 'Number of Female Smokers',
    'Data.Smokers.Male': 'Number of Male Smokers'
})
# Create a CountryConverter instance
cc = CountryConverter()

# Add a new "Continent" column to the DataFrame
filtered_df['Continent'] = filtered_df['Country Name'].apply(lambda x: cc.convert(names=x, to='continent'))

# save to CSV
filtered_df.to_csv(path+'gdp_smoking.csv', encoding='utf-8', index=False)


