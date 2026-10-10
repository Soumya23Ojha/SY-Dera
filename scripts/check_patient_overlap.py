
import pandas as pd

metadata_file = "dataset/raw/skindisnet/SkinDisNet_Metadata.csv"

df = pd.read_csv(metadata_file)

# Assign binary labels
df["Binary_Label"] = df["Diagnosis"].apply(
    lambda label: "Eczema" if label == "Eczema" else "Non-Eczema"
)

print("IMAGE COUNTS")
print(df["Binary_Label"].value_counts())
print()

print("UNIQUE PATIENT COUNTS")
print(df.groupby("Binary_Label")["Patient_id"].nunique())
print()

print("PATIENTS WITH MULTIPLE DIAGNOSES")
diagnoses_per_patient = df.groupby("Patient_id")["Diagnosis"].nunique()
multiple = diagnoses_per_patient[diagnoses_per_patient > 1]

print("Patients with multiple diagnoses:", len(multiple))

if len(multiple) > 0:
    print(multiple.head(10))
