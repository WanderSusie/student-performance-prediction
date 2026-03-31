<![CDATA[<div align="center">

# 🎓 EduPredict AI

### _AI-Powered Student Performance Prediction Dashboard_

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.0-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> 🔮 _Enter a student's study habits, attendance, and background — get an instant AI prediction of their exam score and letter grade._

<br/>

---

</div>

<br/>

## 💡 What is EduPredict AI?

EduPredict AI is a **full-stack machine learning web app** that predicts student academic performance. It takes **8 simple inputs** about a student (like study hours, attendance, and sleep) and delivers:

| | Prediction | Model Used | Output |
|---|---|---|---|
| 📊 | **Exam Score** | Linear Regression | A number between 0–100 |
| 🏅 | **Letter Grade** | Random Forest Classifier | A / B / C / D / F with confidence % |

No external APIs. No cloud dependencies. Everything runs **locally on your machine**.

<br/>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Score Prediction
Enter student data → get a predicted exam score out of 100, powered by **Linear Regression**. Results animate with a smooth count-up effect inside a glowing circle.

</td>
<td width="50%">

### 🏅 Grade Classification
Same inputs → get a letter grade (A through F) with a **probability breakdown** for each class, powered by a **100-tree Random Forest**.

</td>
</tr>
<tr>
<td width="50%">

### 📈 Model Insights Dashboard
See how well the models perform — **R² Score**, **RMSE**, **Accuracy** — plus an interactive **Feature Importance** chart showing which factors matter most.

</td>
<td width="50%">

### 🎨 Premium Dark UI
A sleek **glassmorphism** interface with frosted-glass cards, gradient accents, smooth animations, and the **Inter** font. No bulky frameworks — pure vanilla CSS.

</td>
</tr>
</table>

<br/>

---

## 🏗️ How It Works

The project has three stages that run in sequence:

```
  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
  │  1️⃣  GENERATE     │──────▶│  2️⃣  TRAIN        │──────▶│  3️⃣  SERVE        │
  │                  │       │                  │       │                  │
  │ generate_        │       │ ml_pipeline.py   │       │ app.py           │
  │ dataset.py       │       │                  │       │ (Flask server)   │
  │                  │       │ Trains 2 models: │       │                  │
  │ Creates 1,000    │       │ • Linear Reg.    │       │ Loads models &   │
  │ synthetic        │       │ • Random Forest  │       │ serves the web   │
  │ student records  │       │                  │       │ dashboard with   │
  │                  │       │ Saves .pkl files │       │ real-time        │
  │ ➜ student_       │       │ + metrics.json   │       │ predictions      │
  │   data.csv       │       │ to models/       │       │ on port 5000     │
  └──────────────────┘       └──────────────────┘       └──────────────────┘
```

<br/>

---

## 📂 Project Structure

```
📦 student-performance-prediction/
│
├── 🐍 app.py                     ← Flask server + 3 API endpoints
├── 🤖 ml_pipeline.py             ← Model training & evaluation
├── 🎲 generate_dataset.py        ← Synthetic data generator
├── 📋 requirements.txt           ← Python dependencies (5 packages)
├── 📖 README.md                  ← You are here!
│
├── 📁 data/
│   └── student_data.csv          ← 1,000 generated student records
│
├── 📁 models/
│   ├── linear_model.pkl          ← Trained regression model
│   ├── classifier_model.pkl      ← Trained Random Forest
│   ├── scaler.pkl                ← Feature scaler (StandardScaler)
│   └── metrics.json              ← R², RMSE, accuracy, importances
│
├── 📁 static/
│   ├── css/style.css             ← Dark theme + glassmorphism styles
│   └── js/app.js                 ← Frontend logic (forms, charts, animations)
│
└── 📁 templates/
    └── index.html                ← Single-page dashboard UI
```

<br/>

---

## 🚀 Quick Start

> **Prerequisites:** Python 3.8+ and pip installed.

### Step 1 — Clone & enter the project

```bash
git clone https://github.com/WanderSusie/student-performance-prediction.git
cd student-performance-prediction
```

### Step 2 — Set up virtual environment _(recommended)_

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Generate the dataset

```bash
python generate_dataset.py
```
> ✅ Creates `data/student_data.csv` with 1,000 synthetic student records.

### Step 5 — Train the ML models

```bash
python ml_pipeline.py
```
> ✅ Trains both models, prints metrics, and saves everything to `models/`.

### Step 6 — Launch the dashboard! 🎉

```bash
python app.py
```
> 🌐 Open **http://127.0.0.1:5000** in your browser.

<br/>

---

## 📊 The Dataset — 8 Features That Predict Performance

Every student record contains **8 input features** and **2 targets**:

| # | Feature | Type | Range | What It Represents |
|:-:|---------|:----:|:-----:|-------------------|
| 1 | `study_hours_per_week` | 📐 Continuous | 0 – 40 | Hours spent studying each week |
| 2 | `attendance_percentage` | 📐 Continuous | 40 – 100 | How often the student attends class |
| 3 | `previous_exam_score` | 📐 Continuous | 20 – 100 | Score on the last exam |
| 4 | `assignments_completed` | 🔢 Discrete | 0 – 10 | How many assignments were submitted |
| 5 | `sleep_hours` | 📐 Continuous | 3 – 10 | Average hours of sleep per night |
| 6 | `extracurricular_hours` | 📐 Continuous | 0 – 15 | Weekly time in extracurriculars |
| 7 | `parent_education_level` | 📊 Ordinal | 1 – 4 | 1=HS, 2=Some College, 3=Bachelor's, 4=Master's+ |
| 8 | `internet_access` | ✅ Binary | 0 / 1 | Does the student have internet at home? |

### 🎯 Targets

| Target | Type | How It's Created |
|--------|------|-----------------|
| **exam_score** | Continuous (0–100) | Weighted sum of all 8 features + random noise |
| **grade** | Categorical | A ≥ 90 \| B ≥ 80 \| C ≥ 70 \| D ≥ 60 \| F < 60 |

<details>
<summary>🧮 <strong>Click to see the exact score formula</strong></summary>

<br/>

```
exam_score = 10
    + study_hours       × 0.8     ← strongest positive factor
    + attendance        × 0.3
    + previous_score    × 0.4     ← past performance matters
    + assignments       × 1.5     ← high per-unit weight
    + sleep_hours       × 0.5
    − extracurriculars  × 0.2     ← slight drag if too high
    + parent_education  × 1.5
    + internet_access   × 3.0
    + Gaussian noise σ=5          ← realistic randomness
```

Result is clipped to **[0, 100]**.

</details>

<br/>

---

## 🤖 The ML Models

### Model 1 — Linear Regression _(Score Prediction)_

| | |
|---|---|
| **Algorithm** | `sklearn.linear_model.LinearRegression` |
| **Purpose** | Predict a continuous exam score (0–100) |
| **Input** | 8 features, scaled via StandardScaler |
| **Typical R²** | **~0.98** _(explains 98% of score variance)_ |
| **Typical RMSE** | **~1.7** _(average prediction error of ±1.7 points)_ |

### Model 2 — Random Forest _(Grade Classification)_

| | |
|---|---|
| **Algorithm** | `sklearn.ensemble.RandomForestClassifier` |
| **Trees** | 100 estimators, `random_state=42` |
| **Purpose** | Classify into letter grades (A / B / C / D / F) |
| **Input** | 8 features, scaled via StandardScaler |
| **Typical Accuracy** | **~95%+** |
| **Bonus** | Returns per-class probability distribution |

### Why two models?

| Question You're Asking | Best Model | Example Output |
|------------------------|-----------|---------------|
| _"How many marks will I get?"_ | Linear Regression | **78.5 / 100** |
| _"What grade will I receive?"_ | Random Forest | **Grade B** _(55.7% confidence)_ |

> 💡 **Note:** These metrics are strong because the data is synthetic (generated from a known formula). Real-world data would yield lower scores due to noise, missing variables, and non-linear relationships.

<br/>

---

## 🔌 API Reference

The Flask server exposes **3 endpoints**. All prediction routes accept and return JSON.

<details>
<summary><strong><code>GET /</code></strong> — Serve the dashboard</summary>

Returns the `index.html` template with the full UI.

</details>

<details>
<summary><strong><code>POST /api/predict-score</code></strong> — Predict exam score</summary>

<br/>

**Request:**
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

**Response (200):**
```json
{
  "success": true,
  "predicted_score": 82.3
}
```

</details>

<details>
<summary><strong><code>POST /api/predict-grade</code></strong> — Predict letter grade</summary>

<br/>

**Request:** Same 8-field JSON as above.

**Response (200):**
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

</details>

<details>
<summary><strong><code>GET /api/model-metrics</code></strong> — Get model evaluation data</summary>

<br/>

**Response (200):**
```json
{
  "regression": { "r2_score": 0.9832, "rmse": 1.7345 },
  "classification": { "accuracy": 0.955, "classes": ["A","B","C","D","F"] },
  "features": {
    "names": ["study_hours_per_week", "attendance_percentage", "..."],
    "importances": [0.3412, 0.1567, "..."]
  }
}
```

</details>

<br/>

---

## 🎨 Design & UI

The dashboard uses a custom **glassmorphism** dark theme — no CSS frameworks.

| Design Token | Value | Used For |
|---|---|---|
| 🌑 Background | `#0f111a` | Page base |
| 🔵 Primary Accent | `#00e5ff` | Score tab, buttons, highlights |
| 🟣 Secondary Accent | `#9d4edd` | Grade tab, charts, badges |
| 🔤 Font | [Inter](https://fonts.google.com/specimen/Inter) | All text |
| 🪟 Glass Effect | `backdrop-filter: blur(16px)` | Cards and panels |

### ✨ Micro-Animations

- **Score result** — Animated count-up from 0 to predicted value (1s)
- **Grade result** — Pop-in scale animation with elastic easing
- **Probability bars** — Width transitions from 0% → target (500ms ease)
- **Tab switching** — Fade-in with subtle upward slide
- **Buttons** — Lift on hover with colored shadow bloom

<br/>

---

## 🛠️ Tech Stack at a Glance

```
┌────────────────────────────────────────────────────────────┐
│  FRONTEND            │  BACKEND             │  ML LAYER   │
│                      │                      │             │
│  HTML5               │  Python 3.8+         │  scikit-    │
│  Vanilla CSS3        │  Flask 3.0.3         │  learn      │
│  Vanilla JavaScript  │  Jinja2 Templates    │  1.4.1      │
│  Chart.js (CDN)      │  joblib 1.3.2        │             │
│  Font Awesome 6.4    │                      │  pandas     │
│  Google Fonts        │                      │  numpy      │
│  (Inter)             │                      │             │
└────────────────────────────────────────────────────────────┘
```

<br/>

---

## ⚙️ Configuration

| Setting | Default | How to Change |
|---------|---------|--------------|
| **Port** | `5000` | Edit `app.run(port=XXXX)` in `app.py` |
| **Debug Mode** | `True` | Set `debug=False` for production |
| **Dataset Size** | `1,000` | Call `generate_student_data(5000)` in `generate_dataset.py` |
| **Random Seed** | `42` | Change `np.random.seed()` in generator & pipeline |
| **RF Trees** | `100` | Change `n_estimators` in `ml_pipeline.py` |

<br/>

---

## 🤝 Contributing

Contributions are welcome! Fork → Branch → Commit → PR.

```bash
git checkout -b feature/my-improvement
git commit -m "Add: description of change"
git push origin feature/my-improvement
```

### 💡 Ideas for Improvement

- [ ] Add **cross-validation** to the training pipeline
- [ ] Implement **hyperparameter tuning** (GridSearchCV)
- [ ] Support **real-world datasets** (UCI, Kaggle)
- [ ] Add **responsive CSS** for mobile devices
- [ ] **Containerize** with Docker
- [ ] Deploy to **Render / Railway / Heroku**
- [ ] Add data **visualizations** (distributions, correlations)
- [ ] Implement **user accounts** for saved predictions

<br/>

---

## 📄 License

This project is open source under the **[MIT License](LICENSE)**.

<br/>

---

<div align="center">

**Built with ❤️ using Python · scikit-learn · Flask · Chart.js**

_If you found this useful, consider giving it a ⭐!_

</div>
]]>
