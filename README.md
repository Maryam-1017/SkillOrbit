# SkillOrbit 🚀

> An AI-powered career guidance platform that helps users discover career paths, identify skill gaps, take adaptive skill assessments, simulate live careers, and generate personalized learning roadmaps — all powered by machine learning and real O*NET occupational data.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Modules Explained](#modules-explained)
  - [Backend (Flask API)](#backend-flask-api)
  - [Machine Learning (ML)](#machine-learning-ml)
  - [Frontend](#frontend)
  - [Data](#data)
  - [Models](#models)
  - [Scripts](#scripts)
- [Data Sources](#data-sources)
- [ML Pipeline](#ml-pipeline)
- [API Endpoints](#api-endpoints)
- [File Reference](#file-reference)

---

## Overview

SkillOrbit is a full-stack web application that combines machine learning with occupational science to give users a 360° view of their career trajectory. A user can:

1. Input their current skills or upload a resume.
2. Receive AI-generated career recommendations.
3. See exactly which skills they are missing for their target role (skill gap analysis).
4. Take an adaptive skill test that adjusts question difficulty based on their responses.
5. Simulate what a day/week in their target career looks like.
6. Generate a step-by-step learning roadmap to close their skill gaps.

The backend is built with **Flask**, the ML layer uses **scikit-learn** with models trained on O*NET data, and the frontend is pure HTML/CSS/JavaScript.

---

## Features

| Feature | Description |
|---|---|
| **Career Recommender** | Recommends best-fit careers based on a user's current skill set |
| **Skill Gap Analysis** | Compares user skills against O*NET occupational skill requirements |
| **Adaptive Skill Test** | Dynamically adjusts question difficulty using a trained difficulty model |
| **Resume Analyzer** | Extracts skills from an uploaded resume and maps them to careers |
| **Career Simulator** | Simulates live career scenarios to help users visualize a role |
| **Roadmap Generator** | Produces a personalized, step-by-step learning roadmap |
| **Career Advisor UI** | Interactive advisor page for guided career exploration |

---

## Project Structure

```
SkillOrbit/
│
├── backend/                    # Flask REST API
│   ├── __init__.py
│   ├── app.py                  # Main Flask application & route definitions
│   ├── resume_analyzer.py      # Resume parsing and skill extraction logic
│   └── skill_test.py           # Skill test question serving and scoring logic
│
├── ML/                         # Machine learning modules
│   ├── __init__.py
│   ├── config.py               # Shared ML configuration (paths, constants)
│   ├── shared.py               # Shared utilities used across ML modules
│   ├── recommender.py          # Career recommendation model logic
│   ├── skill_gap.py            # Skill gap computation between user and career
│   ├── roadmap_generator.py    # Generates learning roadmaps from skill gaps
│   ├── career_simulator.py     # Career simulation scenario engine
│   ├── live_simulations.py     # Live/real-time simulation support
│   ├── train_model.py          # Training script for the career recommendation model
│   └── train_difficulty_model.py  # Training script for question difficulty classifier
│
├── frontend/                   # HTML/CSS/JS user interface
│   ├── index.html              # Landing / home page
│   ├── advisor.html            # Career advisor interactive page
│   ├── roadmap.html            # Roadmap visualization page
│   ├── skill_test.html         # Skill assessment test page
│   ├── resume_analyzer.html    # Resume upload and analysis page
│   ├── nav.css                 # Shared navigation styles
│   ├── simulations.js          # JavaScript for career simulations
│   ├── simulations.css         # Styles for simulations page
│   └── static/
│       └── simulations.css     # Static copy of simulation styles
│
├── data/                       # Raw and processed data files
│   ├── careers.csv             # Career metadata (titles, descriptions, skills)
│   ├── questions_metadata.csv  # Skill test questions with metadata
│   └── onet/                   # O*NET occupational database exports
│       ├── Occupation Data.txt     # Job titles and SOC codes
│       ├── Skills.txt              # Skill requirements per occupation
│       ├── Knowledge.txt           # Knowledge requirements per occupation
│       └── Technology Skills.txt   # Technology skills per occupation
│
├── models/                     # Serialized (trained) ML model artifacts
│   ├── career_model.pkl        # Trained career recommendation classifier
│   ├── mlb.pkl                 # MultiLabelBinarizer for skill encoding
│   ├── selector.pkl            # Feature selector used during training
│   └── metrics.json            # Model evaluation metrics (accuracy, F1, etc.)
│
├── scripts/                    # Standalone utility scripts
│   └── predict_difficulty.py   # Script to predict/assign difficulty to questions
│
├── requirements.txt            # Python package dependencies
└── README.md                   # This file
```

---

## Technology Stack

### Backend
- **Python 3.11**
- **Flask** — lightweight REST API framework
- **Gunicorn** — production WSGI server
- **spaCy + en_core_web_sm** — NLP for resume parsing and entity extraction
- **NLTK** — natural language text processing
- **PyMuPDF (fitz) / pdfplumber** — PDF resume reading

### Machine Learning
- **scikit-learn** — career recommendation classifier, feature selection, model training
- **NumPy & pandas** — data wrangling and numerical computation
- **SciPy** — scientific computing support

### Frontend
- **HTML5 / CSS3 / Vanilla JavaScript** — no frontend framework required
- All pages are self-contained; served directly by Flask's static file handler

### Data
- **O*NET Online** — occupational skills, knowledge, and technology requirements
- **CSV** — careers database and question metadata

---

## Getting Started

### Prerequisites

- Python **3.11** or higher
- `pip` package manager
- (Optional) A virtual environment tool such as `venv`

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/SkillOrbit.git
cd SkillOrbit
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Download the spaCy language model** (if not already bundled)

```bash
python -m spacy download en_core_web_sm
```

### Running the Application

**Development mode (Flask built-in server)**

```bash
python backend/app.py
```

The app will start at `http://127.0.0.1:5000` by default.

**Production mode (Gunicorn)**

```bash
gunicorn -w 4 backend.app:app
```

**Retraining the ML models** (optional — pre-trained `.pkl` files are already in `models/`)

```bash
# Retrain the career recommendation model
python ML/train_model.py

# Retrain the question difficulty model
python ML/train_difficulty_model.py
```

---

## Modules Explained

### Backend (Flask API)

#### `backend/app.py`
The entry point of the application. Defines all HTTP routes and wires together the ML modules and frontend. Handles requests for career recommendations, skill tests, resume analysis, roadmap generation, and simulations.

#### `backend/resume_analyzer.py`
Handles resume file uploads (PDF format). Uses **spaCy** and **NLTK** to extract named entities, action verbs, and technical keywords, then maps those to known skills in the O*NET skill taxonomy. Returns a structured list of identified skills.

#### `backend/skill_test.py`
Serves adaptive skill-test questions to the frontend. Selects questions based on the user's current skill domain and dynamically adjusts difficulty based on prior answers (using the difficulty model from `models/`). Scores and returns results at the end of the test.

---

### Machine Learning (ML)

#### `ML/config.py`
Central configuration file. Defines file paths to data and model artifacts, hyperparameters, and any shared constants used across ML modules. Keeping configuration in one place makes it easy to adapt the project to new environments.

#### `ML/shared.py`
Utility functions shared across multiple ML modules — for example, loading the trained models from disk, encoding skill lists with the `MultiLabelBinarizer`, or computing cosine similarity between skill vectors.

#### `ML/recommender.py`
The core career recommendation engine. Loads the trained `career_model.pkl` and `mlb.pkl`. Given a list of user skills, it encodes them and runs prediction to return a ranked list of career matches with confidence scores.

#### `ML/skill_gap.py`
Compares a user's current skill set against the O*NET skill requirements for a chosen career. Returns the skills the user already has, the skills they are missing, and optionally a percentage match score.

#### `ML/roadmap_generator.py`
Takes the output of `skill_gap.py` (the list of missing skills) and generates a prioritized, step-by-step learning roadmap. Skills are ordered by importance to the target role, and each step may include suggested learning resources or categories.

#### `ML/career_simulator.py`
Generates narrative career simulation scenarios. Given a target career and a user's profile, it produces a realistic description of what work in that role looks like — tasks, tools used, daily schedule, and challenges — to help users make informed decisions.

#### `ML/live_simulations.py`
Extends `career_simulator.py` with real-time or streaming simulation support. Useful for progressively rendering long simulation results in the browser without blocking the UI.

#### `ML/train_model.py`
Offline training script for the career recommendation model. Reads `data/careers.csv` and the O*NET data files, encodes skill sets using a `MultiLabelBinarizer`, trains a classifier (e.g. Random Forest or similar), and serializes the trained model and binarizer to `models/`.

#### `ML/train_difficulty_model.py`
Offline training script for the question-difficulty classifier. Reads `data/questions_metadata.csv`, extracts features (question length, domain, user performance history, etc.), and trains a model that predicts difficulty level (easy / medium / hard). Used by the adaptive skill test.

---

### Frontend

All frontend pages are plain HTML with embedded or linked CSS/JS — no build step required.

| File | Purpose |
|---|---|
| `frontend/index.html` | Landing page — introduces SkillOrbit and directs users to features |
| `frontend/advisor.html` | Interactive career advisor — users input skills and get recommendations |
| `frontend/roadmap.html` | Displays the personalized learning roadmap in a visual timeline |
| `frontend/skill_test.html` | Hosts the adaptive skill assessment; communicates with the backend via fetch/AJAX |
| `frontend/resume_analyzer.html` | Resume upload form; sends PDF to backend and displays extracted skills |
| `frontend/simulations.js` | JavaScript logic for rendering career simulations in the browser |
| `frontend/nav.css` | Shared navigation bar styles used across all pages |
| `frontend/simulations.css` | Styling for the simulation display panels |

---

### Data

#### `data/careers.csv`
Contains career records with fields such as career title, description, required skills, and (optionally) salary range or growth outlook. Used to train the recommendation model and populate the frontend career list.

#### `data/questions_metadata.csv`
A dataset of skill-test questions with metadata including question text, skill domain, correct answer, and initial difficulty rating. Used to train the difficulty model and to serve questions during the adaptive test.

#### `data/onet/`
Four files exported from the **O*NET database** (publicly available from the U.S. Department of Labor):

| File | Contents |
|---|---|
| `Occupation Data.txt` | SOC codes, occupation titles, and descriptions |
| `Skills.txt` | Skill importance/level scores per occupation |
| `Knowledge.txt` | Knowledge area importance/level scores per occupation |
| `Technology Skills.txt` | Software and technology tools used per occupation |

---

### Models

Pre-trained model artifacts stored in `models/`. These are loaded at startup and do not need to be retrained unless the underlying data changes.

| File | Description |
|---|---|
| `career_model.pkl` | Trained classifier that maps skill vectors to career recommendations |
| `mlb.pkl` | Fitted `MultiLabelBinarizer` for encoding lists of skills into binary feature vectors |
| `selector.pkl` | Fitted feature selector (e.g. `SelectKBest`) applied after encoding |
| `metrics.json` | Evaluation results from the last training run (accuracy, precision, recall, F1) |

---

### Scripts

#### `scripts/predict_difficulty.py`
A standalone utility script that runs the trained difficulty model over a set of questions and outputs the predicted difficulty level for each. Useful for pre-labelling new questions before adding them to `questions_metadata.csv`.

---

## Data Sources

- **O*NET Online** (https://www.onetcenter.org/database.html) — Open occupational database maintained by the U.S. Department of Labor. Provides standardized skill, knowledge, and technology requirement data for hundreds of occupations.
- **`careers.csv`** — Custom dataset compiled from public career information to supplement O*NET with richer descriptions and structured skill tags.
- **`questions_metadata.csv`** — Custom question bank created for the adaptive skill assessment.

---

## ML Pipeline

```
Raw O*NET Data + careers.csv
        │
        ▼
  Data Preprocessing
  (pandas, cleaning, merging)
        │
        ▼
  Skill Encoding
  (MultiLabelBinarizer → mlb.pkl)
        │
        ▼
  Feature Selection
  (SelectKBest → selector.pkl)
        │
        ▼
  Model Training
  (Classifier → career_model.pkl)
        │
        ▼
  Evaluation → metrics.json
        │
        ▼
  Flask API loads models at startup
        │
        ▼
  User submits skills via frontend
        │
        ▼
  recommender.py → ranked career list
        │
        ▼
  skill_gap.py → missing skills
        │
        ▼
  roadmap_generator.py → learning plan
```

---

## API Endpoints

All endpoints are served by `backend/app.py`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the landing page (`index.html`) |
| `POST` | `/recommend` | Accepts a JSON list of user skills, returns ranked career recommendations |
| `POST` | `/skill-gap` | Accepts user skills + target career, returns missing skills and match % |
| `POST` | `/roadmap` | Accepts missing skills, returns an ordered learning roadmap |
| `POST` | `/analyze-resume` | Accepts a PDF file upload, returns extracted skills |
| `GET` | `/skill-test/question` | Returns the next adaptive test question for the user |
| `POST` | `/skill-test/answer` | Submits an answer, receives score update and next question |
| `POST` | `/simulate` | Accepts a career name, returns a career simulation narrative |

> **Note:** The exact endpoint signatures may vary. Check `backend/app.py` for the authoritative route definitions and expected request/response formats.

---

## File Reference

```
SkillOrbit/
├── backend/app.py                   ← Flask app entry point
├── backend/resume_analyzer.py       ← PDF/resume skill extractor
├── backend/skill_test.py            ← Adaptive test question logic
├── ML/config.py                     ← Paths and constants
├── ML/shared.py                     ← Shared utilities
├── ML/recommender.py                ← Career recommendation inference
├── ML/skill_gap.py                  ← Skill gap computation
├── ML/roadmap_generator.py          ← Learning roadmap construction
├── ML/career_simulator.py           ← Career scenario generator
├── ML/live_simulations.py           ← Streaming simulation support
├── ML/train_model.py                ← Train career model (run offline)
├── ML/train_difficulty_model.py     ← Train difficulty model (run offline)
├── frontend/index.html              ← Home page
├── frontend/advisor.html            ← Career advisor UI
├── frontend/roadmap.html            ← Roadmap display UI
├── frontend/skill_test.html         ← Skill test UI
├── frontend/resume_analyzer.html    ← Resume upload UI
├── frontend/simulations.js          ← Simulation JS logic
├── data/careers.csv                 ← Career dataset
├── data/questions_metadata.csv      ← Question bank
├── data/onet/*.txt                  ← O*NET occupational data
├── models/career_model.pkl          ← Trained recommendation model
├── models/mlb.pkl                   ← Skill binarizer
├── models/selector.pkl              ← Feature selector
├── models/metrics.json              ← Training metrics
├── scripts/predict_difficulty.py    ← Difficulty labelling utility
└── requirements.txt                 ← Python dependencies
```

---

*Built with Python, Flask, scikit-learn, spaCy, and O\*NET data.*