# SkillOrbit — AI-Powered Career Guidance Platform

SkillOrbit is a Flask-based web application that helps students, fresh graduates, and professionals make informed career decisions. It uses a trained Machine Learning model to analyze a user's skills and recommend the most suitable career paths, identify skill gaps, and generate personalized learning roadmaps.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Machine Learning Model](#machine-learning-model)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)

---

## Project Overview

Career decision-making is one of the most challenging tasks for students and professionals. SkillOrbit solves this by combining Machine Learning, Natural Language Processing, and data analytics into a single platform. A user simply enters their skills or uploads their resume — the system handles everything else.

The platform covers four core modules:

1. **Career Recommendation** — ML model predicts best-fit careers based on user skills
2. **Skill Gap Analysis** — identifies which skills the user has and which are missing
3. **Learning Roadmap** — generates a phase-by-phase learning plan for any career
4. **Career Simulator** — shows salary projections and market trends for a chosen career

---

## Features

- **Resume Analyzer** — upload a PDF or DOCX resume; the system extracts skills automatically using NLP (spaCy + fuzzy matching)
- **ML-based Career Recommendations** — trained Random Forest classifier predicts career match with confidence percentage
- **Skill Gap Analysis** — exact and partial skill matching against required skills for any career
- **Personalized Roadmap Generator** — phase-by-phase learning path based on current skill level
- **Career Market Simulator** — 5-year salary projection and demand index based on market trends
- **Petri Net Simulation** — animated visualization of the resume analysis workflow
- **Retrain Endpoint** — `/api/train-model` allows retraining the ML model on demand

---

## Machine Learning Model

### Algorithm
**Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`)

### Why Random Forest?
- Handles high-dimensional binary feature vectors well
- Robust against overfitting with many trees
- Returns `predict_proba()` — confidence scores for every career class
- Works well even with synthetically generated training data

### Training Pipeline

```
careers.csv (60 careers, ~300 unique skills)
        ↓
Synthetic Data Generation (6000 labeled samples)
  - 30 core samples per career (full skill set)
  - 50 partial samples per career (50–85% of skills)
  - 20 noise samples per career (skills + random extras)
        ↓
Feature Encoding — MultiLabelBinarizer
  skills list → binary vector  e.g. ["python","sql"] → [0,1,0,...,1,0]
        ↓
Train / Test Split — 80% train, 20% test (stratified)
        ↓
model.fit(X_train, y_train)  ← actual ML training
        ↓
Evaluation — accuracy_score + classification_report
        ↓
joblib.dump() → models/career_model.pkl
               models/mlb.pkl
```

### Evaluation Metrics
| Metric | Value |
|--------|-------|
| Accuracy | ~98% on test set |
| Evaluation method | Train/test split (stratified) |
| Report | Per-career precision, recall, F1-score |

### At Prediction Time (Flask)
```
User skills input
      ↓
MultiLabelBinarizer.transform()   ← same encoder used in training
      ↓
model.predict_proba()             ← confidence % for each career
      ↓
Top 5 careers ranked by confidence
```

### Model Files
The trained model is **not stored in the repository**. It is generated locally by running the training script. This is standard practice — code is versioned, models are generated fresh.

```
models/                  ← auto-created by train_model.py
├── career_model.pkl     ← trained Random Forest
└── mlb.pkl              ← fitted MultiLabelBinarizer
```

---

## Project Structure

```
SkillOrbit/
├── backend/
│   ├── app.py               # Flask application — all API routes
│   └── resume_analyzer.py   # NLP-based resume parsing + Petri Net
├── data/
│   └── careers.csv          # 60 careers with required skills, salary, demand
├── frontend/
│   ├── index.html           # Landing page
│   ├── advisor.html         # Career advisor (skill input + recommendations)
│   ├── resume_analyzer.html # Resume upload and analysis
│   ├── roadmap.html         # Learning roadmap viewer
│   └── nav.css              # Shared navigation styles
├── ML/
│   ├── train_model.py       # Training script — run this first
│   ├── recommender.py       # Loads trained model, returns career matches
│   ├── skill_gap.py         # Skill gap and partial match analysis
│   ├── roadmap_generator.py # Phase-by-phase roadmap generation
│   └── career_simulator.py  # Salary projection and market trend simulation
├── models/                  # Auto-generated (not in repo)
│   ├── career_model.pkl
│   └── mlb.pkl
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/SkillOrbit.git
cd SkillOrbit
```

### Step 2 — Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### Step 5 — Train the ML model

This step generates the `models/` folder with the trained classifier.

```bash
python ML/train_model.py
```

Expected output:
```
Training model...
Done! Accuracy: 98.5%
Saved to models/career_model.pkl
```

---

## How to Run

```bash
python backend/app.py
```

Open your browser and go to: `http://127.0.0.1:5000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommend` | Get top 5 career matches from skills |
| POST | `/api/skill-gap` | Get skill gap for a specific career |
| POST | `/api/roadmap` | Get learning roadmap for a career |
| GET  | `/api/careers` | List all available careers |
| POST | `/api/career-simulation` | Get salary projection and market trend |
| POST | `/api/analyze-resume` | Upload resume and extract skills |
| POST | `/api/petri-simulate` | Run Petri Net workflow simulation |
| POST | `/api/train-model` | Retrain the ML model on demand |
| POST | `/api/prioritize-skills` | Prioritize missing skills by frequency |

### Example Request — Career Recommendation

```bash
POST /api/recommend
Content-Type: application/json

{
  "skills": ["Python", "Machine Learning", "TensorFlow", "NLP"]
}
```

```json
{
  "user_skills": ["Python", "Machine Learning", "TensorFlow", "NLP"],
  "matches": [
    {
      "career": "NLP Engineer",
      "score": 94.5,
      "salary_min": 85000,
      "salary_max": 150000,
      "demand_level": 9,
      "market_trend": "Rising"
    }
  ]
}
```

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Backend | Flask 3.x |
| ML / Data | scikit-learn, pandas, numpy, joblib |
| NLP | spaCy, rapidfuzz, PyMuPDF |
| Frontend | HTML, CSS, JavaScript |
| Resume Parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Model | Random Forest Classifier |
| Feature Encoding | MultiLabelBinarizer |
| Formal Modeling | Petri Net (custom implementation) |

---


## Notes

- The `models/` directory is excluded from the repository via `.gitignore`
- Always run `python ML/train_model.py` after cloning before starting the server
- The training script generates fresh model files each time it runs
# SkillOrbit

SkillOrbit is a Flask-based career guidance platform that helps users discover career paths from their skills, analyze missing skills, generate learning roadmaps, upload resumes for NLP-based analysis, run career simulations, and take skill tests.

The project combines a Python/Flask backend, plain HTML/CSS/JavaScript frontend pages, CSV/O*NET data, scikit-learn models, resume parsing, and several simulation models used for the Simulation and Modeling workflow.

## Features

- Career recommendations from manually entered skills
- Resume analyzer for PDF/DOCX resumes with skill extraction
- Skill gap analysis with exact and partial skill matching
- Personalized learning roadmaps by career and current skill level
- Career market simulation with salary, demand, automation risk, and growth projections
- Live simulation panels:
  - Petri net resume/workflow simulation
  - Roadmap Petri net simulation
  - Skill gap closure pipeline
  - Career journey timeline
  - Markov chain career progression
  - Job market queue simulation
- Skill test module with standard and adaptive quiz modes
- Difficulty prediction for skill test questions
- Career and quiz data stored in CSV files

## Tech Stack

| Area | Tools |
| --- | --- |
| Backend | Flask, Python |
| Frontend | HTML, CSS, JavaScript, Bootstrap, Chart.js |
| Machine learning | scikit-learn, pandas, numpy, joblib |
| NLP and resume parsing | spaCy, RapidFuzz, PyMuPDF, python-docx |
| Data | CSV, O*NET data files |
| Models | Random Forest, TF-IDF pipelines, MultiLabelBinarizer |

## Project Structure

```text
SkillOrbit/
|-- backend/
|   |-- app.py                 # Flask app, page routes, and API endpoints
|   |-- resume_analyzer.py     # Resume parsing, skill extraction, Petri net workflow
|   |-- skill_test.py          # Skill test, adaptive testing, history, leaderboard
|   `-- __init__.py
|-- ML/
|   |-- config.py              # Shared project/model/data paths
|   |-- recommender.py         # Career recommendation logic
|   |-- skill_gap.py           # Skill gap and match percentage logic
|   |-- roadmap_generator.py   # Career roadmap generation
|   |-- career_simulator.py    # Salary/demand/market simulations
|   |-- live_simulations.py    # Petri, Markov, queue, and pipeline simulations
|   |-- train_model.py         # Career model training script
|   |-- train_difficulty_model.py
|   `-- shared.py              # Shared salary, market, and career helpers
|-- frontend/
|   |-- index.html             # Home page
|   |-- advisor.html           # Skill input and career recommendations
|   |-- resume_analyzer.html   # Resume upload and analysis page
|   |-- roadmap.html           # Learning roadmap page
|   |-- skill_test.html        # Skill test page
|   |-- nav.css
|   |-- simulations.css
|   |-- simulations.js
|   `-- static/
|       `-- simulations.css
|-- data/
|   |-- careers.csv            # Curated careers, skills, salary, demand, risk
|   |-- questions_metadata.csv # Quiz question bank used by skill tests
|   `-- onet/                  # O*NET source files
|-- models/
|   |-- career_model.pkl       # Generated/trained career model
|   |-- mlb.pkl                # Generated skill encoder
|   |-- selector.pkl           # Generated feature selector
|   `-- metrics.json           # Training metrics
|-- scripts/
|   `-- predict_difficulty.py
|-- requirements.txt
`-- README.md
```

## Data and Models

SkillOrbit uses two main data sources:

- `data/careers.csv`: curated career records with required skills, salary range, demand level, automation risk, competition level, job type, market trend, and salary growth rate.
- `data/onet/`: O*NET occupation, skills, knowledge, and technology skill files used by the career model and roadmap logic.

The current career model artifacts live in `models/`:

- `career_model.pkl`
- `mlb.pkl`
- `selector.pkl`
- `metrics.json`

The current `metrics.json` reports:

- Top-1 accuracy: 83.3%
- Top-5 accuracy: 93.54%
- Careers: 911
- Skill features after selection: 163
- Source: O*NET 29.0

If model files are missing, regenerate them with:

```bash
python ML/train_model.py
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements file includes the spaCy English model URL. If spaCy cannot load the model, run:

```bash
python -m spacy download en_core_web_sm
```

### 3. Train or refresh models when needed

Career recommendation model:

```bash
python ML/train_model.py
```

Question difficulty model:

```bash
python ML/train_difficulty_model.py
```

Note: `ML/train_difficulty_model.py` expects `data/skill_test_dataset.csv`. The running app can still use `data/questions_metadata.csv` for tests if that metadata file already exists.

## Run the App

```bash
python backend/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Pages

| Route | Page |
| --- | --- |
| `/` | Home page |
| `/advisor` | Career advisor from entered skills |
| `/roadmap` | Career learning roadmap |
| `/resume-analyzer` | Resume upload and analysis |
| `/skill-test` | Skill quiz and adaptive testing |

## API Endpoints

### Career and Skills

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/recommend` | Return top career matches for a list of skills |
| POST | `/api/skill-gap` | Return exact, partial, and missing skills for a career |
| GET | `/api/careers` | Return grouped career list |
| POST | `/api/roadmap` | Generate a roadmap for a selected career |
| POST | `/api/prioritize-skills` | Prioritize missing skills across career matches |
| POST | `/api/train-model` | Retrain the career recommendation model |

### Resume Analyzer

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/analyze-resume` | Upload a PDF/DOCX resume and extract skills, contact info, matches, and gaps |

### Simulations

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/petri-simulate` | Resume analyzer Petri net workflow |
| POST | `/api/roadmap-simulate` | Roadmap Petri net phase simulation |
| POST | `/api/career-journey-simulate` | Year-by-year career journey simulation |
| POST | `/api/skill-gap-simulate` | Skill gap closure pipeline simulation |
| POST | `/api/markov-simulate` | Markov chain career progression |
| POST | `/api/queue-simulate` | Job market applicant queue simulation |
| POST | `/api/skill-extraction-simulate` | Skill extraction pipeline animation data |
| POST | `/api/career-simulation` | Salary, demand, risk, and market projection data |

### Skill Tests

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/test/skills` | List skills available in the question bank |
| POST | `/api/test/start` | Start a standard or adaptive skill test |
| POST | `/api/test/submit` | Submit standard test answers |
| GET | `/api/test/history` | Get saved test history |
| GET | `/api/test/leaderboard` | Get leaderboard results |
| POST | `/api/test/adaptive/answer` | Submit one adaptive answer and receive the next question |
| POST | `/api/update-user-skills` | Mark skills as known or needing review |
| POST | `/api/admin/predict-difficulty` | Predict difficulty for a question text |

## Example Requests

Career recommendation:

```bash
curl -X POST http://127.0.0.1:5000/api/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"skills\":[\"Python\",\"SQL\",\"Machine Learning\",\"Data Visualization\"]}"
```

Skill gap analysis:

```json
{
  "user_skills": ["Python", "SQL", "Pandas"],
  "career_match": {
    "career": "Data Scientist",
    "required_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas"]
  }
}
```

Start a skill test:

```json
{
  "difficulty": "medium",
  "skill": "Naive Bayes",
  "num_questions": 10,
  "adaptive": false
}
```

## How Matching Works

Career cards and skill gap analysis use shared match percentage logic:

- Exact required skill match counts as `1.0`
- Partial/related match counts as `0.65`
- Score is calculated against the total required skills for the career
- Score is capped at `99.0`

This keeps the career card percentage and detailed skill gap percentage consistent.

## Simulation Notes

- Petri net simulations show step-by-step movement through workflow or roadmap states.
- The skill gap pipeline shows how learning missing skills can increase the match percentage.
- The Markov simulation estimates career stage transitions over time.
- The queue simulation models applicants entering a job market, being screened, and receiving offers based on demand and competition.
- The career simulator projects salary and demand trends for the selected career.

## Common Commands

```bash
# Run the Flask app
python backend/app.py

# Train career recommendation model
python ML/train_model.py

# Train question difficulty model
python ML/train_difficulty_model.py

# Predict difficulty from script helper
python scripts/predict_difficulty.py
```

## Notes for Development

- The app uses `frontend/` as the Flask template folder and also serves it as static files.
- `models/` contains generated artifacts and can become very large.
- `data/test_results.csv` is created when users submit skill tests.
- Resume parsing supports PDF and DOCX inputs.
- Some optional O*NET files such as `Abilities.txt` and `Work Activities.txt` are used by training if present.
- Keep model paths centralized through `ML/config.py`.
