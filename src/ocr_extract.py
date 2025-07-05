import os
import shutil
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
Image.MAX_IMAGE_PIXELS = None  # optional: silence warning

def get_page_count(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        print(f"[!] Could not read PDF page count: {e}")
        return 0

def safe_load_page(pdf_path, page_num, base_dpi=150, pixel_limit=90_000_000):
    dpi = base_dpi
    while dpi >= 72:
        try:
            pages = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num)
            if pages:
                page = pages[0]
                if page.size[0] * page.size[1] <= pixel_limit:
                    return page
                print(f"[!] Page {page_num} too large at {dpi} DPI ({page.size}), trying lower DPI...")
            dpi -= 30
        except Exception as e:
            print(f"[!] Error loading page {page_num} at {dpi} DPI: {e}")
            dpi -= 30
    print(f"[x] Failed to load page {page_num} within safe pixel limits")
    return None

def ocr_pdf_to_text(pdf_path, output_txt_path):
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    text = ""
    total_pages = get_page_count(pdf_path)
    print(f"[i] Detected {total_pages} page(s) in {os.path.basename(pdf_path)}")

    for i in range(1, total_pages + 1):
        print(f"[+] Processing page {i}...")
        page = safe_load_page(pdf_path, i)
        if page:
            try:
                txt = pytesseract.image_to_string(page, lang="eng+hin")
                text += f"\n\n[PAGE {i}]\n{txt}"
            except Exception as e:
                print(f"[!] OCR failed on page {i}: {e}")
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✓] OCR complete: {output_txt_path}")

def batch_ocr():
    input_dir = "data/raw_pdfs/"
    output_dir = "data/extracted_text/"
    processed_dir = "data/processed_pdfs/"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".txt"))

            print(f"\n=== OCR STARTED: {file} ===")
            ocr_pdf_to_text(input_path, output_path)

            # Move PDF to processed folder after OCR
            shutil.move(input_path, os.path.join(processed_dir, file))
            print(f"[→] Moved to processed_pdfs/: {file}")

if __name__ == "__main__":
    batch_ocr()