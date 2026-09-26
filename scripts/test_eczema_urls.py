import pandas as pd
import requests

# Load the Fitzpatrick17k CSV
df = pd.read_csv("dataset/metadata/fitzpatrick17k.csv")

# Select all eczema-related images
eczema_df = df[
    df["label"].str.lower().str.contains("eczema", na=False)
]

print("Total eczema-related images:", len(eczema_df))
print()

# Test the first 10 image URLs
for index, row in eczema_df.head(10).iterrows():

    url = row["url"]

    print("Testing:", url)

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("Status code:", response.status_code)

        if response.status_code == 200:
            print("Result: WORKING")
        else:
            print("Result: NOT WORKING")

    except Exception as e:
        print("Result: ERROR")
        print("Error:", e)

    print("-" * 60)