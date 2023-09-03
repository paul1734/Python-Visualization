import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 

path = "/files/Data/"
os.chdir(path)

df = pd.read_csv(path +'gdp_smoking.csv')
# The value World was still in the Country column, therefore it needed to be 
# dropped for the analysis.
df_world = df.copy()
df_only_continents = df_world[df_world.Continent != 'not found']

# Create displots for each continent

g = sns.displot(
    data=df_only_continents,
    x="Daily Cigarette Consumption", hue="Continent",
    kind="kde", height=6,
    multiple="fill", clip=(0, None),
    palette="tab10",
)
g.fig.suptitle('Distribution of Sum of Total Smokers by Continent Over Years', y=1.02)
