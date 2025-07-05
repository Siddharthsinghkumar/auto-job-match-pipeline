import os
import sys
import json

# Ensure src/ is in the path no matter how script is run
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from layout_detect_blocks import run_layoutparser_and_donut

# 📂 Folder where all newspaper PNGs are organized by PDF name
PDF_IMG_ROOT = "data/pdf2img"

# 📁 Folder to store output job JSONs
OUTPUT_JSON_DIR = "data/jobs_json"
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

# 🔁 Loop through each newspaper folder (e.g., TH Delhi-30-06-2025)
for paper_folder in sorted(os.listdir(PDF_IMG_ROOT)):
    folder_path = os.path.join(PDF_IMG_ROOT, paper_folder)
    if not os.path.isdir(folder_path):
        continue  # Skip non-folder entries

    print(f"\n📰 Processing newspaper: {paper_folder}")
    all_jobs = []

    # 🔁 Process each page PNG
    for img_name in sorted(os.listdir(folder_path)):
        if img_name.lower().endswith(".png"):
            img_path = os.path.join(folder_path, img_name)
            print(f"  📄 Page: {img_name}")
            try:
                jobs = run_layoutparser_and_donut(img_path)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"  [!] Error processing {img_name}: {e}")

    # 💾 Save results
    output_path = os.path.join(OUTPUT_JSON_DIR, f"{paper_folder}_donut_jobs.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_jobs)} job(s) → {output_path}")

    # 📦 Move processed folder to archive
    PROCESSED_DIR = "data/processed_images"
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    dest_path = os.path.join(PROCESSED_DIR, paper_folder)
    if os.path.exists(dest_path):
        print(f"[!] Archive already exists: {dest_path} — skipping move.")
    else:
        os.rename(folder_path, dest_path)
        print(f"📦 Moved processed folder to: {dest_path}")
