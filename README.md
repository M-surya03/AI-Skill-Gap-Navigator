# SkillMap AI — Skill Gap Navigator

> AI-powered resume analysis platform that extracts your skills, compares them against any job description, and generates a personalized week-by-week learning roadmap.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📄 Resume Parsing | Upload PDF, DOCX, or TXT — extracts text, sections, and contact info |
| 🔍 Skill Extraction | Matches 150+ canonical skills via alias-aware pattern matching |
| 📊 Gap Analysis | Identifies matched, missing critical, missing preferred, and transferable skills |
| 🎯 Readiness Score | 0–100% score based on skill coverage + transferability bonus |
| 🗺️ Learning Roadmap | Prerequisite-ordered, week-by-week phases with real learning resources |
| 📈 Visualizations | Readiness gauge, radar chart, category bar chart, gap donut, roadmap timeline |
| 🔄 Transferable Skills | Detects when existing skills partially cover a gap (e.g., Python → ML) |

---

## 🏗️ Architecture

```
Frontend (React + Vite)          Backend (FastAPI)
http://localhost:5173            http://localhost:8000
        │                               │
        │   POST /api/analyze           │
        │──────────────────────────────►│
        │   (resume file + JD text)     │
        │                               │  Resume Parser
        │                               │  → pdfplumber / python-docx
        │                               │
        │                               │  Skill Extractor
        │                               │  → alias index × 150+ skills
        │                               │
        │                               │  Gap Analyzer
        │                               │  → readiness score + transferables
        │                               │
        │                               │  Roadmap Generator
        │                               │  → prerequisite topological sort
        │                               │
        │◄──────────────────────────────│
        │   AnalysisResult JSON         │
```

---

## 📁 Project Structure

```
Skill Gap Navigator/
├── backend/
│   ├── main.py                    # FastAPI app entry
│   ├── routers/
│   │   └── analyze.py             # POST /api/analyze
│   ├── services/
│   │   ├── resume_parser.py       # PDF/DOCX text extraction
│   │   ├── skill_extractor.py     # Skill extraction + gap analysis
│   │   └── roadmap_generator.py   # Prerequisite-ordered roadmap
│   ├── data/
│   │   └── skills_taxonomy.py     # 150+ skills with metadata
│   └── models/
│       └── schemas.py             # Pydantic request/response schemas
│
└── frontend/
    └── src/
        ├── pages/HomePage.tsx     # Main UI
        ├── components/
        │   ├── ResumeUpload.tsx   # Drag-drop uploader
        │   ├── SkillGapCharts.tsx # All visualizations
        │   ├── SkillGapPanel.tsx  # Skill detail panel
        │   └── RoadmapTimeline.tsx# Week-by-week roadmap
        └── api/client.ts          # Axios API client
```

---

## ⚡ Quick Start (Local, No Docker)

### 1. Backend

```powershell
cd backend

# Install Python dependencies
pip install fastapi "uvicorn[standard]" python-multipart pdfplumber python-docx aiofiles

# Start API server
uvicorn main:app --reload --port 8000
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

### 2. Frontend

```powershell
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → http://localhost:5173
```

---

## 🔌 API Reference

### `POST /api/analyze`

Multipart form request:

| Field | Type | Required | Description |
|---|---|---|---|
| `resume` | File | ✅ | PDF, DOCX, or TXT resume |
| `job_title` | string | ✅ | e.g. "Senior Data Scientist" |
| `job_description` | string | ✅ | Full JD text |
| `required_skills_text` | string | ❌ | Override: comma-separated required skills |
| `preferred_skills_text` | string | ❌ | Override: comma-separated preferred skills |

Response: `AnalysisResult` — see `frontend/src/api/client.ts` for full TypeScript types.

---

## 🎨 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 + Vite + TypeScript |
| Charts | Recharts |
| Drag & Drop | react-dropzone |
| Icons | lucide-react |
| Backend | FastAPI (Python 3.13) |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Skill Matching | Custom alias-index (150+ skills) |
| HTTP | Axios |

---

## 📊 Skill Coverage

The taxonomy covers **150+ skills** across these categories:

- Programming Languages (Python, JS, TS, Java, Go, Rust, R, Scala, C/C++)
- Web Frameworks (React, Next.js, Vue, Angular, FastAPI, Django, Flask, Node, Express, Spring)
- AI/ML (Machine Learning, Deep Learning, PyTorch, TensorFlow, NLP, LLMs, Computer Vision, MLOps)
- Data Science (Pandas/NumPy, Data Visualization, Statistics, Linear Algebra)
- Data Engineering (SQL, MongoDB, Apache Spark, Kafka, Airflow)
- Cloud & DevOps (AWS, Azure, GCP, Docker, Kubernetes, Git, CI/CD, Linux)
- Computer Science (DSA, System Design, Networking)

---

## 🔮 Roadmap (Future Enhancements)

- [ ] Neo4j skill knowledge graph (prerequisite traversal at scale)
- [ ] ML-based readiness prediction (XGBoost on HR datasets)
- [ ] SHAP explainability layer ("Why this recommendation?")
- [ ] Multi-candidate comparison for HR teams
- [ ] Course marketplace integration (Coursera, Udemy APIs)
- [ ] LinkedIn profile import
