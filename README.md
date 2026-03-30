# 🎓 Student Performance Prediction Dashboard AI

An AI-powered web dashboard that leverages Machine Learning to predict a student's future exam performance and letter grade based on their study habits, demographics, and historical data.

## 🌟 Features

- **Score Predictor:** Built on a `Linear Regression` model. Accepts study hours, attendance, assignments completed, etc. and outputs an estimation of the final exam score (0–100).
- **Grade Classification:** Built on a `Random Forest Classifier`. Outputs the most likely final letter grade (A, B, C, D, F) alongside class probabilities.
- **Model Insights Dashboard:** Visualizes model metrics like Accuracy and Feature Importance using interactive `Chart.js` components.
- **Glassmorphism UI:** A custom, premium dark-themed interface crafted with modern vanilla CSS and animations. No bulky layout frameworks required.
- **Synthetic Data Pipeline:** Comes with a built-in script designed to generate an arbitrarily large, realistic dataset for learning, testing, and continuous deployment.

## 🛠️ Architecture

- **Backend:** Python + Flask
- **Machine Learning Layer:** scikit-learn (Linear Regression, Random Forest Classifier), pandas, numpy
- **Frontend Dashboard:** HTML5, CSS3, JavaScript (Vanilla JS), Chart.js
- **Model Persistence:** joblib

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.8 or higher installed on your machine.
- `pip` for installing Python dependencies.

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/student-performance-prediction.git
cd student-performance-prediction
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Dataset
Create the synthetic student CSV dataset (`1000 records`).
```bash
python generate_dataset.py
```
*Note: A `data/student_data.csv` file will be created.*

### 4. Train the ML Models
Train the models, evaluate their accuracy, and export the `.pkl` artifact layers.
```bash
python ml_pipeline.py
```
*Note: This creates the `models/` directory alongside `linear_model.pkl` and `classifier_model.pkl`.*

### 5. Launch the Web Application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser to interact with your local instance of EduPredict AI!

---

*Authored by Antigravity*
