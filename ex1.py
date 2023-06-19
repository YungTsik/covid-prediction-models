from matplotlib import pyplot as plt
import pandas as pd 
import seaborn as sns

corona = pd.read_csv("Data/data.csv")

#To check NaN values useprint(corona.isnull().sum().sort_values(ascending=False))

#Rename
corona.rename(columns={"Daily tests": "Tests"}, inplace=True)

#Fill NaN values
#print(corona.isnull().sum().sort_values(ascending=False))
corona.Deaths = corona.groupby("Entity").Deaths.transform(lambda x: x.fillna(method="bfill"))
corona.Cases  = corona.groupby("Entity").Cases.transform(lambda x: x.fillna(method="bfill"))
corona.Tests  = corona.groupby("Entity").Tests.transform(lambda x: x.fillna(method="bfill"))
#bfill = next valid, doesnt fill cases where there is no next valid so we also do the opposite
corona.Deaths = corona.groupby("Entity").Deaths.transform(lambda x: x.fillna(method="ffill"))
corona.Cases  = corona.groupby("Entity").Cases.transform(lambda x: x.fillna(method="ffill"))
corona.Tests  = corona.groupby("Entity").Tests.transform(lambda x: x.fillna(method="ffill"))

corona.Deaths = corona.groupby("Entity").Deaths.transform(lambda x: x.fillna(method='ffill'))
corona.Cases  = corona.groupby("Entity").Cases.transform(lambda x: x.fillna(method='ffill'))
corona.Tests  = corona.groupby("Entity").Tests.transform(lambda x: x.fillna(method='ffill'))
#Drop longitude and latitude
corona.drop(columns=["Longitude","Latitude"],inplace=True)

#export csv

corona.to_csv("Data/alteredData.csv",index=False)

#Calculate pairwise correlation of data
corr = corona.corr().round(2)

usefull_pairs = []
threshfold = 0.7

for r in range(len(corr.values)):
    for c in range(r):
        if corr.values[r][c] > threshfold: 
            usefull_pairs.append([corr.columns[r],corr.columns[c]])

print("\nPrint usefull pairs:\n")
for pair in usefull_pairs:
    print(pair[0],"and",pair[1])       

#Plot correlation heatmap
plt.figure("Pairwise Correlation",figsize=(10,10))
sns.heatmap(corr, annot= True)
plt.tight_layout()
plt.show()


