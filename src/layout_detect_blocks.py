import os
import layoutparser as lp
import pytesseract
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
PDF_IMG_ROOT = "data/pdf2img"

print(f"[DEBUG] Starting job layout extraction pipeline.")

# Load Donut model + processor
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base", use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model.eval()

device = "cpu"
model.to(device)

# Structured prompts for Donut
questions = [
    "What is the job title?",
    "What is the location?",
    "What is the qualification required?",
    "What is the application deadline?",
    "Any notes or preferences mentioned?"
]

def extract_job_info(cropped_img_pil):
    job = {}
    for q in questions:
        prompt = f"<s_docvqa><question>{q}</question><answer>"
        inputs = processor(cropped_img_pil, prompt, return_tensors="pt").to(device)
        output = model.generate(**inputs, max_length=256)

        # ✂️ Extract just the answer portion
        raw_output = processor.batch_decode(output, skip_special_tokens=True)[0]
        clean_answer = raw_output.split("<answer>")[-1].strip()

        # 🧹 Filter out low-quality or empty answers
        if len(clean_answer) < 10 or all(c in ".,-_=<>!~ " for c in clean_answer.strip()):
            print(f"🗑️ Skipped low-quality answer: {clean_answer[:30]}")
            continue

        job[q] = clean_answer

    return job


def run_layoutparser_and_donut(image_path):
    print(f"📄 Loading image: {image_path}")
    image = Image.open(image_path).convert("RGB")

    print("🧠 Loading layout model...")
    model_lp = lp.Detectron2LayoutModel(
        config_path="models/detectron2_publaynet/config.yaml",  # your local file
        model_path="models/detectron2_publaynet/model_final.pth",
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
        device="cpu"
    )

    print("🧠 Running detection...")
    layout = model_lp.detect(image)
    print(f"🧱 Detected {len(layout)} layout blocks")

    jobs = []

    for i, block in enumerate(layout):
        if block.type == "Text":
            x1, y1, x2, y2 = map(int, block.coordinates)
            cropped = image.crop((x1, y1, x2, y2))
            os.makedirs("debug_blocks", exist_ok=True)
            debug_name = f"debug_blocks/{os.path.basename(image_path)}_block_{i}.png"
            cropped.save(debug_name)
            # OCR-based filtering
            text = pytesseract.image_to_string(cropped, lang="eng+hin")
            if any(word in text.lower() for word in ["hiring", "application", "vacancy", "recruitment", "staff", "walk-in"]):
                print(f"[✓] Block {i} may be a job ad — running Donut")
                job_data = extract_job_info(cropped)
                job_data["block_index"] = i
                job_data["page_image"] = image_path
                jobs.append(job_data)

    return jobs
