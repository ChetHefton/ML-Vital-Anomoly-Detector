import os
import wfdb

os.makedirs("data/raw", exist_ok=True)

print("Downloading MIT-BIH Arrhythmia Database (mitdb)...")
wfdb.dl_database("mitdb", dl_dir="data/raw/mitdb")
print("Done. Data is in data/raw/mitdb")