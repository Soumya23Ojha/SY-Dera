# import pandas as pd

# df = pd.read_csv("dataset/metadata/fitzpatrick17k.csv")

# print(df["label"].unique())


import pandas as pd

df = pd.read_csv("dataset/metadata/fitzpatrick17k.csv")

labels = df["label"].dropna().str.lower()

print("Is eczema present?")
print("eczema" in labels.unique())

print("\nLabels containing 'eczema':")
print([label for label in labels.unique() if "eczema" in label])

eczema_df = df[
    df["label"].str.lower() == "eczema"
]

print("\nNumber of eczema images:", len(eczema_df))