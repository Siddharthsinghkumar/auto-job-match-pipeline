
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
├── data/                  # Raw, processed PDFs & text
├── resumes/               # Store your resumes
├── src/                   # Source code
├── models/                # Pretrained layout detection models
├── main.py                # End-to-end runner
├── config.yaml            # API keys & paths
├── requirements.txt       # Python dependencies
└── README.md              # This file
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
