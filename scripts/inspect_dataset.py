
from pathlib import Path
import pandas as pd

# Dataset locations
base = Path("dataset/raw/skindisnet")
image_folder = base / "Preprocessed"
metadata_file = base / "SkinDisNet_Metadata.csv"

print("Checking dataset folders...")
print("Dataset folder exists:", base.exists())
print("Preprocessed folder exists:", image_folder.exists())
print("Metadata file exists:", metadata_file.exists())

if not metadata_file.exists():
    print("\nMetadata CSV not found. Check its filename and location.")
    raise SystemExit

# Load metadata
df = pd.read_csv(metadata_file)

print("\nMetadata shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head().to_string())

print("\nMissing values per column:")
print(df.isnull().sum())

# Show possible disease and class columns
for col in df.columns:
    if any(word in col.lower() for word in
           ["label", "disease", "diagnosis", "class", "condition"]):
        print(f"\nCounts for column: {col}")
        print(df[col].value_counts(dropna=False).to_string())

# Count image files in each folder
if image_folder.exists():
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    images = [
        p for p in image_folder.rglob("*")
        if p.is_file() and p.suffix.lower() in extensions
    ]

    print("\nTotal images in Preprocessed:", len(images))

    print("\nImage counts by subfolder:")
    counts = {}
    for image in images:
        relative = image.relative_to(image_folder)
        folder = relative.parts[0] if len(relative.parts) > 1 else "(root)"
        counts[folder] = counts.get(folder, 0) + 1

    for folder, count in sorted(counts.items()):
        print(f"{folder}: {count}")
