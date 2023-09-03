import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 

path = "/files/Data/"
os.chdir(path)

df = pd.read_csv(path +'gdp_smoking_continents.csv')

# Create displots for each continent
g = sns.displot(
    data=df_only_continents,
    x="Percentage of Total Smokers", hue="Continent",
    kind="kde", height=6,
    multiple="fill", clip=(0, None),
    palette="tab10",
)
g.fig.suptitle('Distribution of Total Smokers by Continent', y=1.02)
