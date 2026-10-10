
from pathlib import Path
import hashlib

image_folder = Path("dataset/raw/skindisnet/Preprocessed")

extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

images = [
    p for p in image_folder.rglob("*")
    if p.is_file() and p.suffix.lower() in extensions
]

hashes = {}
duplicates = []
unreadable = []

print("Checking images...")

for index, path in enumerate(images, start=1):
    try:
        # Check whether the file can be read
        with open(path, "rb") as file:
            data = file.read()

        if not data:
            unreadable.append(str(path))
            continue

        # Check common image file signatures
        valid = False

        if path.suffix.lower() in {".jpg", ".jpeg"}:
            valid = data.startswith(b"\xff\xd8\xff")
        elif path.suffix.lower() == ".png":
            valid = data.startswith(b"\x89PNG\r\n\x1a\n")
        elif path.suffix.lower() == ".webp":
            valid = (
                data.startswith(b"RIFF")
                and data[8:12] == b"WEBP"
            )
        elif path.suffix.lower() == ".bmp":
            valid = data.startswith(b"BM")

        if not valid:
            unreadable.append(str(path))
            continue

        # Detect exact duplicate files
        file_hash = hashlib.md5(data).hexdigest()

        if file_hash in hashes:
            duplicates.append((str(path), hashes[file_hash]))
        else:
            hashes[file_hash] = str(path)

    except Exception as error:
        unreadable.append(f"{path} - {error}")

    if index % 100 == 0:
        print(f"Checked {index}/{len(images)} images")

print("\nIMAGE CHECK REPORT")
print("Total image files:", len(images))
print("Files failing signature/read checks:", len(unreadable))
print("Exact duplicate occurrences:", len(duplicates))

if unreadable:
    print("\nFirst 10 problematic files:")
    for path in unreadable[:10]:
        print(path)

if duplicates:
    print("\nFirst 10 duplicate pairs:")
    for duplicate, original in duplicates[:10]:
        print("Duplicate:", duplicate)
        print("Original:", original)
