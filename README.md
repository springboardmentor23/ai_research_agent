📘 AI System to Automatically Review and Summarize Research Papers
🚀 Project Overview

This project automates the process of fetching, analyzing, comparing, and generating review papers from multiple research papers using AI and NLP techniques.

The system allows users to:

Fetch research papers automatically

Extract text from PDFs

Perform key phrase & similarity analysis

Generate review papers (Local / AI-based)

Evaluate paper quality

Revise generated papers

Download outputs as PDF

The project was developed as part of academic milestones and focuses on building a complete end-to-end research automation pipeline.

🎯 Key Features
🔹 Research Pipeline

Fetch papers based on topic

Download open-access PDFs

Extract text from PDFs

Convert extracted text → JSON

Key phrase extraction

TF-IDF vector creation

Cosine similarity analysis

Cross-paper comparison

🔹 Paper Generation

Local template-based generation

Gemini API-based AI generation

Structured research paper formatting

🔹 Interactive UI (Gradio)

Complete web interface

Pipeline execution with logs

Similarity display

Extracted paper viewer

Revision module

Download options

🔹 Quality & Revision

Quality score evaluation

AI-based revision using user instructions

PDF export for revised papers

🧱 Project Structure
infosysproject/
│
├── app.py                 # Gradio UI (Main Application)
├── main.py                # CLI Pipeline (optional)
│
├── paper_retrieval.py     # Fetch papers API
├── pdf_downloader.py      # Download PDFs
├── text_extractor.py      # Extract PDF text
├── text_to_json.py        # TXT → JSON conversion
├── key_phrases.py         # Key phrase extraction
├── tfidf_vectorizer.py    # TF-IDF creation
├── similarity.py          # Cosine similarity
├── cross_compare.py       # Cross paper comparison
│
├── ai_analysis.py         # AI content extraction
├── common_analysis.py     # Common datasets/methods
├── paper_generator.py     # Paper generation module
├── review_module.py       # Quality scoring & revision
│
├── pdfs/                  # Downloaded papers
├── extracted_texts/       # Extracted text files
├── extracted_texts_json/  # JSON files
├── key_phrases/           # Key phrases output
├── ai_results/            # AI extraction output
│
└── requirements.txt

⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2️⃣ Create Virtual Environment
python -m venv env


Activate:

Windows

env\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 API Setup (Gemini)

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY_HERE

▶️ Running the Project
Run UI Application
py app.py


Open browser:

http://127.0.0.1:7860

🧩 Application Workflow
Step 1 — Pipeline Execution

Enter research topic

Select number of papers (max 10)

Start pipeline

Pipeline performs:

Fetch → Download → Extract → JSON
→ Key Phrases → TF-IDF → Similarity

Step 2 — Generate Review Paper

Choose:

Local Template Mode

API (Gemini) Mode

Generate structured review paper.

Step 3 — Quality Evaluation

Click Get Quality Score to evaluate generated paper.

Step 4 — Extracted Papers Viewer

Select paper from dropdown

View extracted text

Download as PDF

Step 5 — Revision Module

Provide revision instruction

Generate improved paper

Download revised PDF

🎨 UI Features

Interactive dark-gradient interface

Glowing buttons and styled tabs

Real-time pipeline logs

Side-by-side similarity view

🧠 Technologies Used
Category	Tools
Language	Python
UI	Gradio
NLP	TF-IDF, Cosine Similarity
AI	Google Gemini API
PDF Handling	PyPDF2, ReportLab
Data Storage	JSON
📊 Milestone-4 Achievements

✔ Fully interactive application
✔ Integrated end-to-end pipeline
✔ AI paper generation
✔ Quality scoring system
✔ Revision workflow
✔ Downloadable outputs

⚠️ Known Limitations

Some research sites block PDF downloads (403 error).

Scanned PDFs may contain limited text extraction.

Free-tier API has token limits.

🔮 Future Improvements

APA citation formatting

Better semantic analysis

OCR support for scanned PDFs

Cloud deployment

Advanced visual analytics

👨‍💻 Author

Polavaram Hemanth Kumar
Electronics & Communication Engineering
Passionate about IoT, Embedded Systems & AI/ML

⭐ If you like this project

Give it a ⭐ on GitHub 🙂
