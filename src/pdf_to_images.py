from pdf2image import convert_from_path
import os
import shutil

def pdf_to_images(pdf_path, output_base_dir="data/pdf2img", dpi=200):
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(output_base_dir, basename)
    os.makedirs(output_dir, exist_ok=True)

    print(f"[+] Converting PDF: {pdf_path}")
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"[!] Failed to convert {pdf_path}: {e}")
        return

    image_paths = []
    for i, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"{basename}_p{i+1}.png")
        page.save(img_path, "PNG")
        image_paths.append(img_path)
        print(f"  - Saved: {img_path}")

    # Move the PDF to processed_pdfs
    processed_dir = "data/processed_pdfs"
    os.makedirs(processed_dir, exist_ok=True)
    dst_path = os.path.join(processed_dir, os.path.basename(pdf_path))
    shutil.move(pdf_path, dst_path)
    print(f"[→] Moved PDF to processed_pdfs/: {dst_path}")

    return image_paths

if __name__ == "__main__":
    raw_pdf_dir = "data/raw_pdfs"
    found = False
    for fname in os.listdir(raw_pdf_dir):
        if fname.lower().endswith(".pdf"):
            found = True
            pdf_path = os.path.join(raw_pdf_dir, fname)
            print(f"[→] Found PDF: {fname}")
            pdf_to_images(pdf_path)

    if not found:
        print("[!] No PDF files found in data/raw_pdfs/")
