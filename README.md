
# 📄 Job Search AI Pipeline

**AI-powered automation pipeline that downloads newspapers, extracts job listings using OCR and layout detection, translates them, and matches them to your resume using GPT-based semantic filtering. Notifies you via Telegram when relevant jobs are found.**

---

## 🚀 Key Features

✅ Automated newspaper PDF downloads (supports regional & national job newspapers)

✅ Layout-aware OCR extraction (using PyMuPDF, pdf2image, Detectron2 / LayoutParser, Donut, or Tesseract)

✅ Translation of non-English job listings (Hindi, Marathi, etc.) to English

✅ NLP-powered job parsing & keyword extraction

✅ Resume-job semantic matching using OpenAI GPT (zero-shot/few-shot inference)

✅ Automatic Telegram alerts for relevant job matches

✅ Daily pipeline automation (cron/Task Scheduler)

---

## 🔧 Tech Stack

| Domain                      | Tools / Libraries                              |
|-----------------------------|------------------------------------------------|
| 📥 PDF Download             | requests, curl                                 |
| 📄 OCR / Image Processing   | PyMuPDF, pdf2image, pytesseract, Donut         |
| 🧱 Layout Detection         | Detectron2 (PubLayNet), LayoutParser           |
| 🌐 Translation              | googletrans, IndicTrans (planned)              |
| 🧠 AI Matching              | OpenAI GPT-4 API, Zero-shot prompting          |
| 🤖 Notifications            | Telegram Bot API                               |
| 🔁 Automation               | cron (Linux), Task Scheduler (Windows)         |

---

## 🔁 Pipeline Workflow

```
Download PDFs
     ↓
Convert PDF to Images
     ↓
Detect Layout Blocks
     ↓
Run OCR or Donut to extract text
     ↓
Translate to English (if required)
     ↓
Parse job listings from text
     ↓
Check match with resume using GPT
     ↓                 ↓
Match Found       No Match
     ↓                 ↓
Send Alert       Delete PDF
```

---

## 📂 Folder Structure

```
job-search-ai-pipeline/
├── data/
│   ├── raw_pdfs/               # Directly downloaded PDFs (raw)
│   ├── processed_pdfs/         # PDFs after layout detection / cleaning
│   ├── processed_images/       # Images extracted from PDFs (for OCR/layout detection)
│   ├── pdf2img/                # Temp folder for intermediate PDF → image conversions
│   ├── extracted_text/         # OCR-extracted raw text from images
│   └── jobs_json/              # Parsed, structured job data in JSON format
│
├── resumes/
│   ├── resume_ee.txt           # Electrical resume
│   └── resume_aiml.txt         # AI/ML resume
│
├── src/
│   ├── download_pdfs.py        # Script to download daily newspaper PDFs
│   ├── pdf2img.py              # Convert PDFs to images (using pdf2image, etc.)
│   ├── layout_detect_blocks.py # Detect text/image blocks in pages (Detectron2, LayoutParser, etc.)
│   ├── layout_donut_pipeline.py# Donut/Transformer-based OCR + layout-aware extraction
│   ├── parse_jobs.py           # Rule-based or ML/NLP-based job extraction
│   ├── match_resume.py         # Resume-job matching with OpenAI GPT or local LLM
│   └── feedback_loop.py        # (Future) Self-learning from feedback
│
├── models/
│   └── detectron2_publaynet/   # Pretrained layout detection models (optional)
│
├── main.py                     # Pipeline orchestrator (runs all steps end-to-end)
├── config.yaml                  # Config: API keys, paths, hyperparameters, newspaper URLs
├── README.md                    # Project overview, setup, usage instructions
└── requirements.txt             # List of dependencies
```


---

## ⚙️ Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/<your-username>/job-search-ai-pipeline.git
   cd job-search-ai-pipeline
   ```
   ### 🔗 Pretrained Layout Detection Model (PubLayNet)

Download the pretrained Detectron2 PubLayNet model (~330 MB):

```bash
mkdir -p models/detectron2_publaynet
wget -O models/detectron2_publaynet/model_final.pth "https://www.dropbox.com/s/dgy9c10wykk4lq4/model_final.pth?dl=1"
wget -O models/detectron2_publaynet/config.yml "https://raw.githubusercontent.com/Layout-Parser/layout-parser/main/layoutparser/data/PubLayNet/faster_rcnn_R_50_FPN_3x.yaml"
```
   
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Add your configuration in `config.yaml` (OpenAI key, Telegram bot token, etc.)

4. Run the pipeline manually:
   ```bash
   python main.py
   ```

Or schedule it daily via `cron` or Windows Task Scheduler.

---

## 🛡️ License

Licensed under the **MIT License** — free for personal and educational use.

---

## 📬 Future Improvements
- Add self-learning feedback loop
- Support multiple resume profiles (EE + AI/ML)
- Deploy as a microservice or Streamlit app
- Add support for more newspapers
