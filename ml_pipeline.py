import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

def run_pipeline():
    print("Starting ML Pipeline...")
    
    # 1. Load Data
    data_path = 'data/student_data.csv'
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Run generate_dataset.py first.")
        return
    
    df = pd.read_csv(data_path)
    
    # Features & Targets
    X = df.drop(['exam_score', 'grade'], axis=1)
    y_reg = df['exam_score']
    y_clf = df['grade']
    
    # Keep feature names for frontend insights
    feature_names = X.columns.tolist()
    
    # Scale Features (Important for LR)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train-Test Split (Shared for consistency)
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X_scaled, y_reg, y_clf, test_size=0.2, random_state=42
    )
    
    # --- 2. Train Linear Regression ---
    print("\nTraining Linear Regression Model...")
    reg_model = LinearRegression()
    reg_model.fit(X_train, y_reg_train)
    
    # Evaluate
    y_reg_pred = reg_model.predict(X_test)
    r2 = r2_score(y_reg_test, y_reg_pred)
    rmse = np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))
    print(f"Linear Regression R2 Score: {r2:.4f}")
    print(f"Linear Regression RMSE: {rmse:.4f}")
    
    # --- 3. Train Random Forest Classifier ---
    print("\nTraining Random Forest Classifier...")
    # Use RandomForest for robust multiclass classification
    clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_model.fit(X_train, y_clf_train)
    
    # Evaluate
    y_clf_pred =clf_model.predict(X_test)
    accuracy = accuracy_score(y_clf_test, y_clf_pred)
    print(f"Classifier Accuracy: {accuracy:.4f}")
    print("\nClassification Report:\n", classification_report(y_clf_test, y_clf_pred))
    
    # Get feature importances
    importances = clf_model.feature_importances_
    
    # --- 4. Save Models & Scaler ---
    os.makedirs('models', exist_ok=True)
    joblib.dump(reg_model, 'models/linear_model.pkl')
    joblib.dump(clf_model, 'models/classifier_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Save a metrics report for the frontend to consume
    metrics = {
        'regression': {
            'r2_score': round(r2, 4),
            'rmse': round(rmse, 4)
        },
        'classification': {
            'accuracy': round(accuracy, 4),
            'classes': list(clf_model.classes_)
        },
        'features': {
            'names': feature_names,
            'importances': [round(float(imp), 4) for imp in importances]
        }
    }
    
    import json
    with open('models/metrics.json', 'w') as f:
        json.dump(metrics, f)
        
    print("\nPipeline Complete! Models and artifacts saved to 'models/' directory.")

if __name__ == "__main__":
    run_pipeline()
