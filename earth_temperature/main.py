import pandas as pd

temp_df = pd.read_csv("10_EarthTempAnomalies.csv")
def get_bin(abnormally):
    return int((abnormally+0.9)/0.3)
temp_dict = {}
month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i, row in temp_df.iterrows():
    for m in month:
        if "-".join([str(row["Year"]), m]) not in temp_dict:
            temp_dict["-".join([str(row["Year"]), m])] = {}
        temp_dict["-".join([str(row["Year"]), m])][row["Hemisphere"]] = row[m]

save_dict = {"year": [], "month":[], "global":[], "northern": [], "southern": [], "bin": []}
for k, v in temp_dict.items():
    save_dict['year'].append(int(k.split("-")[0]))
    save_dict['month'].append(month.index(k.split("-")[1])+1)
    save_dict['global'].append(v['Global'])
    save_dict['northern'].append(v['Northern'])
    save_dict['southern'].append(v['Southern'])
    save_dict['bin'].append(get_bin(v['Global']))

save_df = pd.DataFrame.from_dict(save_dict)
save_df.to_csv("preprocessed_data.csv")



