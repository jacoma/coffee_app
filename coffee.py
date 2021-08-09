from os import X_OK
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from scipy.stats import norm

temp = pd.read_csv("coffee_details.csv")
countries = pd.read_csv("countries.csv")
temp_ratings = pd.read_csv("coffee_ratings.csv")

coffee_df = temp.loc[:, "coffee_id":"Roaster Notes"]

# Roaster is always available; Roast is pretty sparse.
na_means = coffee_df.isna().mean(axis=0).reset_index()

plt_df = pd.DataFrame({"Columns": na_means["index"], "Prop_NA": na_means[0]})

plt.figure(figsize=[8, 8])
plt.bar(x="Columns", height="Prop_NA", data=plt_df)
plt.show()

# Dropping 'Roast'
coffee_df = coffee_df.drop("Roast")

# How many coffees from each country.
coffee_df.groupby("Country")["coffee_id"].count().reset_index()

# Replace values with 'Blend' to just 'Blend'
idx = coffee_df["Country"].str.contains("Blend", na=False)

coffee_df.loc[idx, "Country2"] = "Blend"

coffee_df.loc[-idx, "Country2"] = coffee_df.loc[-idx, "Country"]

coffee_df[coffee_df["Country2"] == "Various"] = "Blend"

# Count groups
coffee_countries_df = pd.merge(
    left=coffee_df,
    right=countries,
    how="left",
    left_on="Country2",
    right_on="Country"
)

continents_count = (
    coffee_countries_df.groupby("Continent")["coffee_id"].count().reset_index()
)
totals = coffee_countries_df.coffee_id.count()

continents_count["prop"] = np.round((continents_count.coffee_id / totals) * 100)

plt_df = continents_count.sort_values("prop")

### Bar Plot for percentage of coffee by Continent
fig, ax = plt.subplots()
p1 = ax.barh(y="Continent", width="prop", data=plt_df)
plt.title("Number of Coffees by Country")
plt.xlabel("Percentage of Coffees Tasted")
plt.ylabel("Continent")
plt.bar_label(p1, padding=5)
plt.grid(False)
ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()


### Ratings of Coffee
coffee_ratings = pd.merge(
    left=coffee_countries_df,
    right=temp_ratings,
    how="inner",
    left_on="coffee_id",
    right_on="ID",
)

coffee_ratings["Rating"].isna().mean()
coffee_ratings_noNA = coffee_ratings[coffee_ratings["Rating"].isna() == False]

### Histogram of Ratings
num_bins = 10
n, bins, patches = plt.hist(
    "Rating", data=coffee_ratings_noNA, bins=num_bins, facecolor="blue", alpha=0.5
)
plt.show()
# Most ratings fall at 3 or 4.


### Plot Ratings vs. Continent
ratings_agg = (
    coffee_ratings_noNA.groupby("Continent")
    .agg({"Rating": "mean"})
    .reset_index()
    .sort_values("Rating")
)

ratings_agg["Rating"] = np.round(ratings_agg["Rating"], 1)

fig, ax = plt.subplots()
p1 = ax.barh(y="Continent", width="Rating", data=ratings_agg)
plt.title("Average Rating by Continent")
plt.xlabel("Average Rating (1-5)")
plt.ylabel("Continent")
plt.bar_label(p1, padding=5)
plt.grid(False)
ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()


### Create binary ratings >= 4
coffee_ratings_noNA["high_rating_flag"] = 0
coffee_ratings_noNA.loc[coffee_ratings_noNA["Rating"] >= 4, "high_rating_flag"] = 1


### Plot Ratings vs. Continent
ratings_agg = (
    coffee_ratings_noNA.groupby("Continent")
    .agg({"high_rating_flag": "mean"})
    .reset_index()
    .sort_values("high_rating_flag")
)

ratings_agg["high_rating_flag"] = np.round(ratings_agg["high_rating_flag"], 1)

fig, ax = plt.subplots()
p1 = ax.barh(y="Continent", width="high_rating_flag", data=ratings_agg)
plt.title("Average Rating by Continent")
plt.xlabel("Average Rating (1-5)")
plt.ylabel("Continent")
plt.bar_label(p1, padding=5)
plt.grid(False)
ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()


### Plot Ratings vs. Country
ratings_agg = (
    coffee_ratings_noNA.groupby("Country2")
    .agg({"high_rating_flag": "mean", "coffee_id": "count"})
    .reset_index()
    .sort_values("high_rating_flag")
)

ratings_agg["high_rating_flag"] = np.round(ratings_agg["high_rating_flag"], 1)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.barh(y="Country2", width="high_rating_flag", data=ratings_agg)
ax1.title("Average Rating by Country")
ax1.xlabel("Average Rating (1-5)")
ax1.ylabel("Country")
ax2.bar_label(padding=5)

ax2.barh(y="Country2", width="coffee_id", data=ratings_agg)
ax2.title("Count by Country")
ax2.xlabel("Count")
ax2.ylabel("Country")
ax2.bar_label(padding=5)
ax2.grid(False)

ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()


### Extract flavor notes
notes_df = coffee_ratings_noNA['Roaster Notes'].str.split(', ', expand=True)

coffee_notes_df = pd.concat([coffee_ratings_noNA, notes_df], axis=1)

coffee_melt_df = pd.melt(
    coffee_notes_df, 
    id_vars='coffee_id', 
    value_vars=[0,1,2,3,4,5,6],
    var_name='notes',
    value_name='value'
)

coffee_melt_df = pd.merge(
    left=coffee_ratings_noNA.drop('Roaster Notes', 1),
    right=coffee_melt_df,
    how='inner',
    on='coffee_id'
)

## TODO: replace 'ries' with 'ry'
coffee_notes_clean_df = coffee_melt_df[coffee_melt_df['value'].isna()==False]
coffee_notes_clean_df.value = coffee_notes_clean_df.value.str.lower()

plt_df = coffee_notes_clean_df.groupby('value').agg({'coffee_id':'count'}).reset_index().sort_values('coffee_id')
fig, ax = plt.subplots(figsize=(12,12))
p1 = ax.barh(y="value", width="coffee_id", data=plt_df[plt_df.coffee_id > 1])
plt.title("Number of Ratings with Flavor Note")
plt.xlabel("Number of Ratings")
plt.ylabel("Flavor Note")
plt.bar_label(p1, padding=5)
plt.grid(False)
ax.get_xaxis().set_visible(False)  # Remove x-axis line

for spine in ax.spines:
    ax.spines[spine].set_visible(False)

plt.show()

plt_df[plt_df.coffee_id == 1]
