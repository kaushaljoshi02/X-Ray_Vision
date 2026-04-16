import os
import zipfile
import shutil
import random

# -----------------------------
# STEP 1: CREATE MAIN FOLDERS
# -----------------------------
classes = ["COVID", "Normal", "Pneumonia", "Tuberculosis"]

for cls in classes:
    os.makedirs(f"dataset_all/{cls}", exist_ok=True)

# -----------------------------
# STEP 2: DOWNLOAD DATASETS
# -----------------------------
print("📥 Downloading datasets...")

os.system("kaggle datasets download -d paultimothymooney/chest-xray-pneumonia")
os.system("kaggle datasets download -d tawsifurrahman/covid19-radiography-database")
os.system("kaggle datasets download -d tawsifurrahman/tuberculosis-tb-chest-xray-dataset")

# -----------------------------
# STEP 3: EXTRACT ZIP FILES
# -----------------------------
print("📦 Extracting datasets...")

os.makedirs("data_raw", exist_ok=True)

for file in os.listdir():
    if file.endswith(".zip"):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall("data_raw")

# -----------------------------
# STEP 4: SAFE COPY FUNCTION
# -----------------------------
def copy_images(src, dst):
    if not os.path.exists(src):
        print(f"❌ Path not found: {src}")
        return

    count = 0
    for root, dirs, files in os.walk(src):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                shutil.copy(os.path.join(root, f), dst)
                count += 1

    print(f"✅ Copied {count} images from {src} → {dst}")

# -----------------------------
# STEP 5: AUTO-DETECT PATHS
# -----------------------------
print("🔍 Copying images...")

# Pneumonia dataset (handle nested folders)
copy_images("data_raw/chest_xray/train/NORMAL", "dataset_all/Normal")
copy_images("data_raw/chest_xray/train/PNEUMONIA", "dataset_all/Pneumonia")

copy_images("data_raw/chest_xray/chest_xray/train/NORMAL", "dataset_all/Normal")
copy_images("data_raw/chest_xray/chest_xray/train/PNEUMONIA", "dataset_all/Pneumonia")

# COVID dataset
copy_images("data_raw/COVID-19_Radiography_Dataset/COVID", "dataset_all/COVID")
copy_images("data_raw/COVID-19_Radiography_Dataset/NORMAL", "dataset_all/Normal")

# TB dataset (multiple possible paths)
copy_images("data_raw/Tuberculosis", "dataset_all/Tuberculosis")
copy_images("data_raw/TB_Chest_Radiography_Database/Tuberculosis", "dataset_all/Tuberculosis")

# -----------------------------
# STEP 6: CREATE FINAL SPLIT
# -----------------------------
print("🔀 Splitting dataset...")

for split in ["train", "val", "test"]:
    for cls in classes:
        os.makedirs(f"dataset/{split}/{cls}", exist_ok=True)

def split_data(src, train, val, test):
    files = os.listdir(src)
    random.shuffle(files)

    n = len(files)
    train_split = int(0.7 * n)
    val_split = int(0.85 * n)

    for i, f in enumerate(files):
        src_path = os.path.join(src, f)

        if i < train_split:
            dst = os.path.join(train, f)
        elif i < val_split:
            dst = os.path.join(val, f)
        else:
            dst = os.path.join(test, f)

        shutil.copy(src_path, dst)

for cls in classes:
    split_data(
        f"dataset_all/{cls}",
        f"dataset/train/{cls}",
        f"dataset/val/{cls}",
        f"dataset/test/{cls}"
    )

print("🎉 DATASET READY SUCCESSFULLY!")