import pandas as pd

df = pd.read_csv("dataset/metadata/fitzpatrick17k.csv")

print("Number of images:", len(df))
print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())