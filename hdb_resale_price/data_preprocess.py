import pandas as pd
import json
import numpy as np

# 50th Percentile
def q25(x):
    return x.quantile(0.25)

# 90th Percentile
def q75(x):
    return x.quantile(0.75)

def split_time(year_month):
    return year_month.split("-")

def story_range_map(x):
    sr = x.split(" ")
    low = int(sr[0])
    high = int(sr[-1])
    if high < 10:
        return "low storey"
    elif high < 20:
        return "medium storey"
    else:
        return "high storey"

central_areas = ['DOWNTOWN CORE', 'MARINA EAST', 'MARINA SOUTH', 'MUSEUM', 'NEWTON', 'ORCHARD', 'OUTRAM',
                 'RIVER VALLEY', 'ROCHOR', 'SINGAPORE RIVER', 'STRAITS VIEW']

hdb_df = pd.read_csv("raw_data.csv")
hdb_df["story_highlow"] = hdb_df.apply(lambda row: story_range_map(row["storey_range"]), axis=1)
hdb_df["year"] = hdb_df.apply(lambda row: split_time(row["month"])[0], axis=1)
hdb_df = hdb_df.loc[hdb_df['year'] == "2017"]

print(hdb_df["storey_range"].unique())

town_df = hdb_df.groupby(['town'], as_index=False).agg({'floor_area_sqm':'sum','resale_price':'sum'}).reset_index()

town_df["price_per_sqm"] = town_df.apply(lambda row: row['resale_price']/row["floor_area_sqm"], axis=1)
town_price = {}
for i, r in town_df.iterrows():
    town_price[r["town"]] = r["price_per_sqm"]
print(town_price)

with open("response.json") as f:
    res = json.load(f)
    for a in res:
        if a["pln_area_n"] in town_price:
            a["price"] = town_price[a["pln_area_n"]]
        elif a["pln_area_n"] in central_areas:
            a["price"] = town_price['CENTRAL AREA']
        elif a["pln_area_n"] == "KALLANG":
            a["price"] = town_price['KALLANG/WHAMPOA']
        else:
            a["price"] = 0

with open("response_with_price.json", "w") as f:
    json.dump(res, f, indent=4)

hdb_df["price_per_sqm"] = hdb_df.apply(lambda row: row['resale_price']/row["floor_area_sqm"], axis=1)
# hdb_df["scaled_resale_price"] = hdb_df["price_per_sqm"]/1000000
story_df = hdb_df.groupby('story_highlow').agg(max=('price_per_sqm', np.max), min=('price_per_sqm', np.min),
                                             quan25=('price_per_sqm', q25), quan75=('price_per_sqm', q75),
                                             median=('price_per_sqm', np.median))
story_df.to_csv("boxplot.csv", float_format='%.1f')

remaining_lease_df = hdb_df.groupby('remaining_lease').agg(mean=('price_per_sqm', np.mean))
remaining_lease_df.to_csv("remaining_lease.csv", float_format='%.1f')