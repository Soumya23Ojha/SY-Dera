import pandas as pd

# Load the Fitzpatrick17k dataset
df = pd.read_csv("dataset/metadata/fitzpatrick17k.csv")

# Find all labels containing the word "eczema"
eczema_df = df[
    df["label"].str.lower().str.contains("eczema", na=False)
]

# Show how many images belong to each eczema label
print("Eczema label counts:")
print(eczema_df["label"].value_counts())

# Show the columns available for these images
print("\nColumns:")
print(eczema_df.columns)

# Show the first 5 eczema records
print("\nFirst 5 eczema records:")
print(eczema_df.head())