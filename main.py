import os
import sys
import subprocess

RAW_PDF_DIR = "data/raw_pdfs"
PDF_IMG_DIR = "data/pdf2img"
PROCESSED_IMG_DIR = "data/processed_images"
JOB_JSON_DIR = "data/jobs_json"

def make_dirs():
    os.makedirs(RAW_PDF_DIR, exist_ok=True)
    os.makedirs(PDF_IMG_DIR, exist_ok=True)
    os.makedirs(PROCESSED_IMG_DIR, exist_ok=True)
    os.makedirs(JOB_JSON_DIR, exist_ok=True)

def run_script(script_name):
    print(f"\n🚀 Running {script_name} ...")
    result = subprocess.run(["python", f"src/{script_name}"], check=False)
    if result.returncode != 0:
        print(f"[❌] {script_name} exited with error.")
        sys.exit(1)

def move_processed_folders():
    for folder in os.listdir(PDF_IMG_DIR):
        src = os.path.join(PDF_IMG_DIR, folder)
        dst = os.path.join(PROCESSED_IMG_DIR, folder)
        if os.path.isdir(src):
            print(f"📦 Moving {folder} → processed_images/")
            os.rename(src, dst)

if __name__ == "__main__":
    print("📌 Newspaper Job Extraction Pipeline")
    print("📅 Please ensure today's PDFs are in:", RAW_PDF_DIR)

    make_dirs()

    input("\n📥 Step 1: Place all PDFs in 'data/raw_pdfs/' and press [Enter] to continue...")

    run_script("pdf_to_images.py")  # Convert PDFs to images
    run_script("layout_donut_pipeline.py")  # Extract jobs using LayoutParser + Donut

    move_processed_folders()

    print("\n✅ All Done!")
    print(f"🔍 Extracted job JSONs saved in: {JOB_JSON_DIR}")
    print("🗂️ All processed images moved to:", PROCESSED_IMG_DIR)
