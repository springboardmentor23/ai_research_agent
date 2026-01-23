# AI Research Agent – Automated Literature Review System

## 1. Project Overview

The **AI Research Agent** is an automated system designed to simplify the early stages of a **systematic literature review**.  
The system automates research paper discovery, dataset creation, text extraction, and cross-paper comparison using Natural Language Processing (NLP) techniques.

This project was developed as part of an **internship training program** and is divided into two milestones aligned with weekly learning objectives.

---

## 2. Project Objectives

- Reduce manual effort in searching and reviewing research papers
- Automatically collect and organize research papers by topic
- Extract meaningful sections from PDFs
- Identify key research contributions
- Compare papers quantitatively using NLP similarity metrics

---

## 3. Technologies Used

- **Python**
- **Semantic Scholar API** (public access)
- **arXiv API** (fallback source)
- **Requests**
- **TF-IDF Vectorizer**
- **Cosine Similarity**
- **JSON for structured datasets**

---
## 4. Milestone 1 (Week 1–2): Paper Search & Dataset Creation

### 4.1 Implemented Features

- User input for number of research topics
- Automated paper search using:
  - Semantic Scholar (primary)
  - arXiv (fallback when rate-limited)
- Open-access PDF downloading
- Topic-wise dataset creation
- Graceful handling of:
  - API rate limits
  - Missing PDFs
  - Empty search results

### 4.2 Outputs

- `cleaned_dataset.json`
- Downloaded PDFs stored in `/pdfs`
- Topic-wise paper metadata

### 4.3 Learning Outcomes

- API integration
- Error handling
- Dataset structuring for NLP pipelines

---

## 5. Milestone 2 (Week 3–4): Text Analysis & Cross-Paper Comparison

### 5.1 Implemented Features

- PDF text extraction
- Section-wise extraction:
  - Abstract
  - Methodology
  - Conclusion
- Key-finding extraction using research phrases
- TF-IDF vectorization
- Cosine similarity computation
- Validation of extracted sections

### 5.2 Outputs

- Section-wise text files
- Key findings per paper
- Cosine similarity matrix
- `similarity_results.json`

### 5.3 Learning Outcomes

- NLP preprocessing
- Feature extraction using TF-IDF
- Quantitative similarity comparison
- Result validation

---

## 6. How to Run the Project

### Step 1: Activate Virtual Environment: 
env\Scripts\activate
### Step 2: Run the main program:
python main.py

## 7. Sample Output

- **Research papers printed topic-wise**

- **Downloaded PDFs saved locally**

- **Extracted sections validated**

- **Cosine similarity matrix displayed in terminal**

- **Results saved as JSON for further analysis**
