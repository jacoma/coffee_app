import matplotlib.pyplot as plt
import pandas as pd
from dfply import *

temp = pd.read_csv("coffee-env\coffee_details.csv")
countries = pd.read_csv("coffee-env\countries.csv")

coffee_df = temp.loc[:, 'Name':'Roaster Notes']

# Roaster is always available; Roast is pretty sparse.
na_means = coffee_df.isna().mean(axis=0).reset_index()

plt_df = pd.DataFrame({'Columns': na_means['index'], 'Prop_NA':na_means[0]})

plt.figure(figsize= [8,8])
plt.bar(x = 'Columns', height = 'Prop_NA', data = plt_df)
plt.show()

# Dropping 'Roast'
coffee_df = (
    coffee_df 
    >> drop('Roast')
    )

# How many coffees from each country.
coffee_df.groupby('Country')['Roaster'].count().reset_index()

(coffee_df >>
    group_by(X.Country) >>
    summarize(counts = X.Roaster.count())
    )

# Replace values with 'Blend' to just 'Blend'
idx = coffee_df['Country'].str.contains("Blend", na=False)

coffee_df.loc[idx, 'Country2'] = 'Blend'

coffee_df.loc[-idx, 'Country2'] = coffee_df.loc[-idx, 'Country']

coffee_df[coffee_df['Country2'] == 'Various'] = 'Blend'

# Count groups
coffee_countries_df = pd.merge(coffee_df, countries, how='left', left_on = 'Country2', right_on = 'Country')

continents_count = coffee_countries_df.groupby('Continent')['Roaster'].count().reset_index()
totals = coffee_countries_df.Roaster.count()

plt_df = (
    continents_count >> 
    mutate(prop = np.round(X.Roaster/totals*100, 1)) >>
    arrange(X.prop)
)


### Bar Plot for percentage of coffee by Continent
fig, ax = plt.subplots()
p1 = ax.barh(y = 'Continent', width = 'prop', data = plt_df, color = 'b')
plt.title('Number of Coffees by Country')
plt.xlabel('Percentage of Coffees Tasted')
plt.ylabel('Continent')
plt.bar_label(p1, padding = 5)
plt.grid(False)
ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()


### Ratings of Coffee
coffee_continents_df.Rating.head()


