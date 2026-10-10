
from pathlib import Path
import pandas as pd
import re

# Dataset paths
base = Path("dataset/raw/skindisnet")
image_folder = base / "Preprocessed"
metadata_file = base / "SkinDisNet_Metadata.csv"

# Load metadata
df = pd.read_csv(metadata_file)

# Count unique patients in each diagnosis
print("UNIQUE PATIENTS BY DIAGNOSIS")
print(df.groupby("Diagnosis")["Patient_id"].nunique())
print()

# Build a lookup of image filenames
extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

image_lookup = {}

for path in image_folder.rglob("*"):
    if path.is_file() and path.suffix.lower() in extensions:
        folder = path.parent.name
        filename = path.stem

        # Ignore spaces and symbols when matching names
        key = (
            re.sub(r"[^a-z0-9]", "", folder.lower()),
            re.sub(r"[^a-z0-9]", "", filename.lower())
        )

        image_lookup[key] = path

# Match CSV records to image files
matched = 0
unmatched = []

for _, row in df.iterrows():
    folder_key = re.sub(
        r"[^a-z0-9]", "", row["Folder_name"].lower()
    )
    image_key = re.sub(
        r"[^a-z0-9]", "", str(row["Image_id"]).lower()
    )

    key = (folder_key, image_key)

    if key in image_lookup:
        matched += 1
    else:
        unmatched.append(
            (row["Folder_name"], row["Image_id"])
        )

print("IMAGE MATCHING RESULTS")
print("Metadata records:", len(df))
print("Matched images:", matched)
print("Unmatched records:", len(unmatched))

if unmatched:
    print("\nFirst 10 unmatched records:")
    for item in unmatched[:10]:
        print(item)
