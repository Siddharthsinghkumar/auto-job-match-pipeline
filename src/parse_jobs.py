import os
import re
import json

def parse_job_block(text_block):
    job = {}

    # Match job title
    title_match = re.search(
        r"(?i)(recruitment|vacancy|applications invited|hiring|opening).*?(for)?\s*(.*(?:engineer|officer|manager|technician|assistant|intern))",
        text_block)
    if title_match:
        job["title"] = title_match.group(3).strip()

    # Match qualification or eligibility
    qual_match = re.search(
        r"(?i)(qualification|eligibility)[:\-]?\s*([^\n]+)",
        text_block)
    if qual_match:
        job["qualification"] = qual_match.group(2).strip()

    # Match deadline
    date_match = re.search(
        r"(?i)(last date|apply by|deadline)[:\-]?\s*([0-9]{1,2}\s\w+\s20\d{2})",
        text_block)
    if date_match:
        job["deadline"] = date_match.group(2).strip()

    # Match location
    loc_match = re.search(
        r"(?i)(location|posting|place)[:\-]?\s*([^\n]+)",
        text_block)
    if loc_match:
        job["location"] = loc_match.group(2).strip()

    # Match links or application sites
    link_match = re.search(r"(https?://[^\s]+|www\.[^\s]+|apply at\s+[^\s]+)", text_block, re.IGNORECASE)
    if link_match:
        job["link"] = link_match.group(0).strip()

    # Match fallback info (notes)
    fallback = re.findall(r"(?i)(apply soon|check details|visit site|read more|see website|refer official site)", text_block)
    if fallback:
        job["notes"] = " | ".join(set(fallback)).strip()

    return job if "title" in job else None  # Only return if title is found

def parse_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("\n\n")
    jobs = []
    for block in blocks:
        parsed = parse_job_block(block)
        if parsed:
            jobs.append(parsed)
    return jobs

def batch_parse(input_dir="data/extracted_text/", output_dir="data/jobs_json/"):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file.replace(".txt", ".json"))

            print(f"[+] Parsing {file}")
            jobs = parse_text_file(input_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            print(f"[✓] Extracted {len(jobs)} job(s) → {output_path}")

if __name__ == "__main__":
    batch_parse()
