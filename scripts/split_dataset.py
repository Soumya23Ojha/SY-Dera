
import random
import shutil
from pathlib import Path

import pandas as pd

# Dataset paths
BASE = Path("dataset/raw/skindisnet")
IMAGE_FOLDER = BASE / "Preprocessed"
METADATA_FILE = BASE / "SkinDisNet_Metadata.csv"
OUTPUT = Path("dataset/processed")

random.seed(42)

# Read metadata
df = pd.read_csv(METADATA_FILE)

df["Binary_Label"] = df["Diagnosis"].apply(
    lambda x: "Eczema" if x == "Eczema" else "Non-Eczema"
)

# Stop if the output folder already contains files
if OUTPUT.exists() and any(p.is_file() for p in OUTPUT.rglob("*")):
    raise SystemExit(
        "Output already contains files. Check dataset/processed "
        "before running this script again."
    )

# Find images using folder name and image ID
image_lookup = {}

for path in IMAGE_FOLDER.rglob("*"):
    if path.is_file() and path.suffix.lower() in {
        ".jpg", ".jpeg", ".png", ".webp", ".bmp"
    }:
        key = (path.parent.name.strip(), path.stem.strip())
        image_lookup[key] = path

# Match metadata rows to image files
records = []

for _, row in df.iterrows():
    key = (str(row["Folder_name"]).strip(),
           str(row["Image_id"]).strip())

    if key not in image_lookup:
        raise SystemExit(f"Image not found for metadata entry: {key}")

    records.append({
        "source": image_lookup[key],
        "Patient_id": row["Patient_id"],
        "Diagnosis": row["Diagnosis"],
        "Binary_Label": row["Binary_Label"],
        "Image_id": row["Image_id"],
        "Folder_name": row["Folder_name"]
    })

data = pd.DataFrame(records)

# Ensure each patient belongs to only one binary class
labels_per_patient = data.groupby("Patient_id")["Binary_Label"].nunique()

if (labels_per_patient > 1).any():
    raise SystemExit("Some patients have conflicting binary labels.")

# Group all images belonging to each patient
patient_groups = {}

for patient_id, group in data.groupby("Patient_id"):
    label = group["Binary_Label"].iloc[0]
    patient_groups.setdefault(label, []).append(
        (patient_id, group.to_dict("records"))
    )

splits = ["train", "validation", "test"]
ratios = {"train": 0.70, "validation": 0.15, "test": 0.15}
assignments = []

# Split each class separately while keeping patients together
for label, groups in patient_groups.items():
    random.shuffle(groups)
    groups.sort(key=lambda item: len(item[1]), reverse=True)

    total_images = sum(len(rows) for _, rows in groups)
    targets = {
        split: total_images * ratios[split]
        for split in splits
    }
    counts = {split: 0 for split in splits}

    for patient_id, rows in groups:
        # Choose the split that is furthest below its target
        chosen_split = min(
            splits,
            key=lambda s: counts[s] / max(targets[s], 1)
        )

        counts[chosen_split] += len(rows)

        for row in rows:
            row["Split"] = chosen_split
            assignments.append(row)

# Copy images and create the manifest
manifest_rows = []

for row in assignments:
    label_folder = row["Binary_Label"].lower().replace("-", "_")
    destination = OUTPUT / row["Split"] / label_folder / row["source"].name

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(row["source"], destination)

    manifest_rows.append({
        "source_path": str(row["source"]),
        "destination_path": str(destination),
        "Patient_id": row["Patient_id"],
        "Diagnosis": row["Diagnosis"],
        "Binary_Label": row["Binary_Label"],
        "Split": row["Split"],
        "Image_id": row["Image_id"],
        "Folder_name": row["Folder_name"]
    })

manifest = pd.DataFrame(manifest_rows)
manifest.to_csv(OUTPUT / "split_manifest.csv", index=False)

# Verify patient separation
patient_split_counts = manifest.groupby("Patient_id")["Split"].nunique()

if (patient_split_counts > 1).any():
    raise SystemExit("ERROR: A patient appears in multiple splits.")

# Display results
print("\nDATASET SPLIT COMPLETED")
print("Total images:", len(manifest))
print("\nImage counts by split:")
print(manifest["Split"].value_counts())

print("\nImage counts by class and split:")
print(pd.crosstab(manifest["Split"], manifest["Binary_Label"]))

print("\nUnique patients by split:")
print(manifest.groupby("Split")["Patient_id"].nunique())

print("\nPatient overlap check: PASSED")
print("Manifest saved to:", OUTPUT / "split_manifest.csv")
