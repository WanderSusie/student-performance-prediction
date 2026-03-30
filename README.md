<![CDATA[# 🎓 EduPredict AI — Student Performance Prediction Dashboard

> An AI-powered web dashboard that leverages Machine Learning to predict a student's future exam performance and letter grade based on their study habits, demographics, and historical data.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Pipeline](#-data-pipeline)
- [Machine Learning Models](#-machine-learning-models)
- [API Reference](#-api-reference)
- [Frontend Design](#-frontend-design)
- [Quick Start](#-quick-start)
- [Configuration & Environment](#%EF%B8%8F-configuration--environment)
- [Usage Guide](#-usage-guide)
- [Performance & Metrics](#-performance--metrics)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

**EduPredict AI** is a full-stack web application that combines supervised machine learning with a glassmorphism-themed dashboard to provide actionable academic predictions. Given a set of 8 input features describing a student's habits and background, the system outputs:

1. A **numerical exam score** (0–100) via Linear Regression.
2. A **letter grade classification** (A / B / C / D / F) with per-class probability distributions via Random Forest.

The project is fully self-contained: it ships with its own synthetic data generator, model training pipeline, and a production-ready Flask web server — no external datasets or APIs required.

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| **Score Predictor** | Linear Regression model estimates a final exam score (0–100) from 8 student features. |
| **Grade Classifier** | Random Forest Classifier outputs the most likely letter grade (A–F) alongside per-class probability bars. |
| **Model Insights Dashboard** | Live metrics display — R² Score, RMSE, Classifier Accuracy — plus an interactive Feature Importance bar chart via Chart.js. |
| **Glassmorphism UI** | Premium dark-themed interface with frosted-glass cards, gradient accents, and smooth micro-animations. |
| **Synthetic Data Pipeline** | Deterministic, seed-controlled generator produces realistic, correlated student records at any scale. |
| **RESTful API** | Clean JSON API endpoints for both prediction models and model metrics — easy to integrate with external tools. |
| **Animated Results** | Score counting animation and grade pop-in effects give a polished, interactive experience. |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER (Browser)                              │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │     Frontend: HTML5 + Vanilla CSS + JavaScript + Chart.js │     │
│   │     (Glassmorphism UI with tab-based navigation)          │     │
│   └────────────────────────┬──────────────────────────────────┘     │
│                            │  HTTP (JSON)                           │
└────────────────────────────┼────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                       Flask Web Server (app.py)                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────┐ │
│  │  GET /            │  │ POST /api/       │  │ GET /api/         │ │
│  │  Serve index.html │  │ predict-score    │  │ model-metrics     │ │
│  │                   │  │ predict-grade    │  │                   │ │
│  └──────────────────┘  └───────┬──────────┘  └────────┬──────────┘ │
│                                │                       │            │
│  ┌─────────────────────────────▼───────────────────────▼──────────┐ │
│  │                   Model Artifacts (models/)                    │ │
│  │  linear_model.pkl │ classifier_model.pkl │ scaler.pkl │ metrics│ │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                  Offline Pipeline (run once)                         │
│  generate_dataset.py ────▶ data/student_data.csv                    │
│  ml_pipeline.py ─────────▶ models/*.pkl + models/metrics.json       │
└─────────────────────────────────────────────────────────────────────┘
```

**Data flow summary:**

1. `generate_dataset.py` creates a synthetic CSV dataset.
2. `ml_pipeline.py` reads that CSV, trains two models (regression + classifier), scales features, and serializes everything to `models/`.
3. `app.py` loads the serialized artifacts at startup and serves predictions through a Flask API.
4. The browser-based frontend consumes those API endpoints to display results in real-time.

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.8+, Flask 3.0.3 | Web server, API routing, template rendering |
| **Machine Learning** | scikit-learn 1.4.1 | Linear Regression, Random Forest Classifier, StandardScaler |
| **Data Processing** | pandas 2.2.2, numpy 1.26.4 | DataFrame operations, numerical computation |
| **Model Persistence** | joblib 1.3.2 | Serialization of trained models and scaler |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | UI structure, styling, interactivity |
| **Charts** | Chart.js (CDN) | Feature Importance bar visualization |
| **Typography** | Google Fonts (Inter) | Modern, clean typeface |
| **Icons** | Font Awesome 6.4.0 (CDN) | Navigation and UI iconography |

---

## 📂 Project Structure

```
student-performance-prediction/
├── app.py                    # Flask web server & API endpoints
├── ml_pipeline.py            # Model training, evaluation, and export
├── generate_dataset.py       # Synthetic student data generator
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusion rules
├── README.md                 # This documentation
│
├── data/
│   └── student_data.csv      # Generated synthetic dataset (1,000 records)
│
├── models/
│   ├── linear_model.pkl      # Trained Linear Regression model (~696 B)
│   ├── classifier_model.pkl  # Trained Random Forest model (~4.3 MB)
│   ├── scaler.pkl            # Fitted StandardScaler (~1.2 KB)
│   └── metrics.json          # Evaluation metrics for the frontend
│
├── static/
│   ├── css/
│   │   └── style.css         # Glassmorphism theme & component styles
│   └── js/
│       └── app.js            # Frontend logic (forms, fetch, charts)
│
└── templates/
    └── index.html            # Main single-page dashboard template
```

---

## 📊 Data Pipeline

### Synthetic Data Generator (`generate_dataset.py`)

The project uses a **deterministic, seed-controlled** data generator instead of relying on external datasets. This ensures:
- **Reproducibility** — `np.random.seed(42)` guarantees identical output across runs.
- **Privacy** — No real student data is ever used.
- **Scalability** — Adjust `num_students` parameter to generate any volume of records.

### Feature Definitions

| # | Feature | Type | Range | Description |
|---|---------|------|-------|-------------|
| 1 | `study_hours_per_week` | Continuous | 0 – 40 | Weekly hours spent studying |
| 2 | `attendance_percentage` | Continuous | 40 – 100 | Class attendance rate (%) |
| 3 | `previous_exam_score` | Continuous | 20 – 100 | Score on the prior exam |
| 4 | `assignments_completed` | Discrete | 0 – 10 | Number of assignments turned in |
| 5 | `sleep_hours` | Continuous | 3 – 10 | Average nightly sleep |
| 6 | `extracurricular_hours` | Continuous | 0 – 15 | Weekly extracurricular time |
| 7 | `parent_education_level` | Ordinal | 1 – 4 | 1 = HS, 2 = Some College, 3 = Bachelor's, 4 = Master's+ |
| 8 | `internet_access` | Binary | 0 / 1 | Whether the student has home internet |

### Target Variables

| Target | Type | Derivation |
|--------|------|------------|
| `exam_score` | Continuous (0–100) | Weighted linear combination of features + Gaussian noise (σ = 5) |
| `grade` | Categorical (A–F) | Thresholded from `exam_score`: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, F < 60 |

### Score Formula

```
exam_score = 10
    + study_hours_per_week × 0.8
    + attendance_percentage × 0.3
    + previous_exam_score × 0.4
    + assignments_completed × 1.5
    + sleep_hours × 0.5
    − extracurricular_hours × 0.2
    + parent_education_level × 1.5
    + internet_access × 3.0
    + 𝒩(0, 5)        ← Gaussian noise
```

The resulting score is clipped to the [0, 100] range. This formula ensures that the features with the strongest impact are **study hours**, **previous exam score**, and **assignments completed** — consistent with real-world education research.

---

## 🤖 Machine Learning Models

### Training Pipeline (`ml_pipeline.py`)

The pipeline executes the following steps in order:

```
Load CSV → Split Features/Targets → StandardScaler fit → 80/20 Train-Test Split
    ├── Train Linear Regression → Evaluate (R², RMSE) → Serialize .pkl
    └── Train Random Forest Classifier (100 trees) → Evaluate (Accuracy) → Serialize .pkl
          └── Extract Feature Importances
Save scaler.pkl + metrics.json
```

### Model 1: Linear Regression (Score Prediction)

| Property | Value |
|----------|-------|
| **Algorithm** | `sklearn.linear_model.LinearRegression` |
| **Input** | 8 standardized features |
| **Output** | Continuous exam score, clamped to [0, 100] |
| **Evaluation Metric** | R² Score, RMSE |
| **Use Case** | "How much will this student likely score?" |

### Model 2: Random Forest Classifier (Grade Prediction)

| Property | Value |
|----------|-------|
| **Algorithm** | `sklearn.ensemble.RandomForestClassifier` |
| **Hyperparameters** | `n_estimators=100`, `random_state=42` |
| **Input** | 8 standardized features |
| **Output** | Letter grade (A/B/C/D/F) + class probability vector |
| **Evaluation Metric** | Accuracy Score, Classification Report |
| **Use Case** | "What letter grade is this student most likely to receive?" |

### Feature Scaling

All features are normalized using `sklearn.preprocessing.StandardScaler` (zero-mean, unit-variance). The fitted scaler is persisted to `scaler.pkl` so that inference-time inputs receive identical transformations.

### Model Artifacts

After training, four files are saved to `models/`:

| File | Size | Contents |
|------|------|----------|
| `linear_model.pkl` | ~696 B | Serialized Linear Regression coefficients |
| `classifier_model.pkl` | ~4.3 MB | Serialized 100-tree Random Forest |
| `scaler.pkl` | ~1.2 KB | Fitted StandardScaler (mean + std per feature) |
| `metrics.json` | ~416 B | R², RMSE, Accuracy, feature names & importances |

---

## 🔌 API Reference

The Flask server exposes three endpoints. All prediction endpoints accept and return **JSON**.

### `GET /`

Serves the main dashboard HTML page.

---

### `POST /api/predict-score`

Predicts a numerical exam score using the Linear Regression model.

**Request Body:**

```json
{
  "study_hours_per_week": 15,
  "attendance_percentage": 85,
  "previous_exam_score": 75,
  "assignments_completed": 8,
  "sleep_hours": 7.5,
  "extracurricular_hours": 5,
  "parent_education_level": 3,
  "internet_access": 1
}
```

**Success Response (200):**

```json
{
  "success": true,
  "predicted_score": 82.3
}
```

**Error Response (400/500):**

```json
{
  "error": "Model not trained yet"
}
```

---

### `POST /api/predict-grade`

Predicts a letter grade and per-class probabilities using the Random Forest Classifier.

**Request Body:** Same schema as `/api/predict-score`.

**Success Response (200):**

```json
{
  "success": true,
  "predicted_grade": "B",
  "probabilities": {
    "A": 12.3,
    "B": 55.7,
    "C": 25.1,
    "D": 5.8,
    "F": 1.1
  }
}
```

---

### `GET /api/model-metrics`

Returns pre-computed evaluation metrics and feature importance data.

**Success Response (200):**

```json
{
  "regression": {
    "r2_score": 0.9832,
    "rmse": 1.7345
  },
  "classification": {
    "accuracy": 0.955,
    "classes": ["A", "B", "C", "D", "F"]
  },
  "features": {
    "names": ["study_hours_per_week", "attendance_percentage", "..."],
    "importances": [0.3412, 0.1567, "..."]
  }
}
```

---

## 🎨 Frontend Design

### Design Philosophy

The UI follows a **glassmorphism** design language paired with a dark color scheme, creating a premium, modern aesthetic.

### Design Tokens (CSS Custom Properties)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-dark` | `#0f111a` | Page background |
| `--bg-card` | `rgba(22, 25, 37, 0.6)` | Glass card base color |
| `--primary-blue` | `#00e5ff` | Primary accent (Score Prediction) |
| `--primary-purple` | `#9d4edd` | Secondary accent (Grade Prediction) |
| `--text-main` | `#f8f9fa` | Body text |
| `--text-muted` | `#adb5bd` | Subdued labels and descriptions |
| `--border-color` | `rgba(255,255,255,0.1)` | Subtle glass borders |

### Layout

- **Sidebar** (260px fixed) — Vertical navigation with icon + label links.
- **Content Area** (flex remaining) — Tab-pane system with fade-in animations.
- **Glass Cards** — Each content panel uses `backdrop-filter: blur(16px)` with 20px border-radius.

### Tab Views

| Tab | Component | Description |
|-----|-----------|-------------|
| **Predict Score** | Form → Animated Score Circle | Inputs map to Linear Regression; result displays as an animated count-up inside a glowing circle. |
| **Predict Grade** | Form → Grade Badge + Probability Bars | Inputs map to Random Forest; result pops in as a large letter with horizontal probability bars. |
| **Model Insights** | Metrics Cards + Chart.js Bar Chart | Displays R², RMSE, Accuracy as highlight values. Feature Importance rendered as a styled bar chart. |

### Animations

- **Tab transitions:** `fadeIn` keyframe (opacity 0→1, translateY 10px→0) over 400ms.
- **Score result:** Count-up animation over 1000ms with 30 discrete steps.
- **Grade result:** Scale pop (0.5→1.0) using a `cubic-bezier(0.175, 0.885, 0.32, 1.275)` easing curve.
- **Probability bars:** Width transition from 0% to target with 500ms ease.
- **Buttons:** Lift effect on hover (`translateY(-2px)`) with colored box-shadow bloom.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed on your machine
- **pip** for installing Python dependencies

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-prediction.git
cd student-performance-prediction
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the Dataset

```bash
python generate_dataset.py
```

✅ Creates `data/student_data.csv` with **1,000 synthetic** student records.

### 5. Train the ML Models

```bash
python ml_pipeline.py
```

✅ Trains both models, prints evaluation metrics, and saves artifacts to `models/`.

**Expected output:**

```
Starting ML Pipeline...

Training Linear Regression Model...
Linear Regression R2 Score: 0.98xx
Linear Regression RMSE: 1.xxxx

Training Random Forest Classifier...
Classifier Accuracy: 0.9xxx

Classification Report:
              precision    recall  f1-score   support
           A       ...       ...       ...       ...
           B       ...       ...       ...       ...
           C       ...       ...       ...       ...
           D       ...       ...       ...       ...
           F       ...       ...       ...       ...

Pipeline Complete! Models and artifacts saved to 'models/' directory.
```

### 6. Launch the Web Application

```bash
python app.py
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## ⚙️ Configuration & Environment

### Port Configuration

The Flask server runs on **port 5000** by default. To change it, modify the last line in `app.py`:

```python
app.run(debug=True, port=8080)  # Change to desired port
```

### Debug Mode

Debug mode is **enabled** by default for development (`debug=True`). For production:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Dataset Size

To generate more or fewer records, pass a custom count to the generator:

```python
# In generate_dataset.py, change:
generate_student_data(5000)  # Generate 5,000 records instead of 1,000
```

### Dependencies

All pinned versions are specified in `requirements.txt`:

```
Flask==3.0.3
scikit-learn==1.4.1.post1
pandas==2.2.2
numpy==1.26.4
joblib==1.3.2
```

---

## 📖 Usage Guide

### Predicting a Score

1. Click **"Predict Score"** in the sidebar.
2. Fill in the 8 input fields (study hours, attendance, etc.).
3. Click **"Predict Expected Score"**.
4. The predicted score animates into the glowing circle on the right.

### Predicting a Grade

1. Click **"Predict Grade"** in the sidebar.
2. Fill in the same 8 input fields.
3. Click **"Predict Letter Grade"**.
4. The predicted grade pops into the badge, and probability bars appear below showing confidence per grade.

### Viewing Model Insights

1. Click **"Model Insights"** in the sidebar.
2. View R² Score, RMSE, and Classification Accuracy on the left.
3. The Feature Importance chart loads on the right, showing which features the Random Forest classifier weighs most heavily.

---

## 📈 Performance & Metrics

The models achieve strong predictive performance on the synthetic dataset:

| Model | Metric | Typical Value |
|-------|--------|---------------|
| Linear Regression | R² Score | ~0.98 |
| Linear Regression | RMSE | ~1.7 |
| Random Forest Classifier | Accuracy | ~95%+ |

> **Note:** High performance is expected since the synthetic data is generated from a known linear formula. With real-world data, expect lower R² and accuracy due to non-linear relationships, noise, and missing variables.

### Why Two Models?

| Scenario | Model | Output |
|----------|-------|--------|
| "How many marks will I get?" | Linear Regression | 78.5 / 100 |
| "What grade will I receive?" | Random Forest | Grade B (55.7% confidence) |

Linear Regression provides a continuous numerical estimate, while the Random Forest Classifier frames the same prediction as a discrete, interpretable category with confidence levels.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch:** `git checkout -b feature/my-improvement`
3. **Commit your changes:** `git commit -m "Add: description of change"`
4. **Push to branch:** `git push origin feature/my-improvement`
5. **Open a Pull Request**

### Suggested Improvements
- [ ] Add cross-validation to the training pipeline
- [ ] Implement hyperparameter tuning (GridSearchCV)
- [ ] Support real-world datasets (UCI, Kaggle)
- [ ] Add responsive CSS for mobile devices
- [ ] Implement user authentication for saved predictions
- [ ] Add data visualization (score distributions, correlations)
- [ ] Containerize with Docker for easy deployment
- [ ] Deploy to a cloud platform (Heroku, Railway, Render)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Built with ❤️ using Python, scikit-learn, Flask & Chart.js</strong>
</p>
]]>
