import os
import fitz  # PyMuPDF
from keybert import KeyBERT
import pandas as pd

# Initialize KeyBERT model
kw_model = KeyBERT('all-MiniLM-L6-v2')

# Path to folder with PDFs
pdf_folder = "project_briefs/"
data = []

# Loop through PDF files
for i, filename in enumerate(os.listdir(pdf_folder), start=1):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        doc = fitz.open(pdf_path)

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        # Extract top 5 keywords/phrases (1 to 3 words)
        keywords = kw_model.extract_keywords(
            full_text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            top_n=5
        )
        keywords_str = ", ".join([kw[0] for kw in keywords])

        data.append({
            "S.No": i,
            "Project Text": full_text.strip(),
            "Extracted Keywords": keywords_str
        })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("extracted_projects.csv", index=False, encoding="utf-8")
print("CSV created: extracted_projects.csv")
