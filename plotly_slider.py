#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 11:09:55 2023

@author: -
"""

import plotly.express as px
import pandas as pd
import os

path = YOUR_PATH_HERE
os.chdir(path)

df = pd.read_csv(path +'gdp_smoking.csv')


fig = px.scatter(df, x="GDPpC", y="Percentage of Total Smokers", animation_frame="Year", animation_group="Country Name",
           size="Daily Cigarette Consumption", color="Continent", hover_name="Country Name",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[0,100])

fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.show()
