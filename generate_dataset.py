import pandas as pd
import numpy as np
import os

def generate_student_data(num_students=1000):
    np.random.seed(42)
    
    # 1. Generate Input Features
    study_hours_per_week = np.random.uniform(0, 40, num_students)
    attendance_percentage = np.random.uniform(40, 100, num_students)
    previous_exam_score = np.random.uniform(20, 100, num_students)
    assignments_completed = np.random.randint(0, 11, num_students)
    sleep_hours = np.random.uniform(3, 10, num_students)
    extracurricular_hours = np.random.uniform(0, 15, num_students)
    parent_education_level = np.random.choice([1, 2, 3, 4], num_students, p=[0.2, 0.4, 0.3, 0.1])
    internet_access = np.random.choice([0, 1], num_students, p=[0.1, 0.9])
    
    # 2. Generate Target (exam_score)
    # Give realistic weights to features to create correlation
    base_score = 10
    score_noise = np.random.normal(0, 5, num_students)
    
    exam_score = (
        base_score +
        (study_hours_per_week * 0.8) +
        (attendance_percentage * 0.3) +
        (previous_exam_score * 0.4) +
        (assignments_completed * 1.5) +
        (sleep_hours * 0.5) -
        (extracurricular_hours * 0.2) + # slight negative impact if too high, mostly neutral 
        (parent_education_level * 1.5) +
        (internet_access * 3.0) +
        score_noise
    )
    
    # Clip exam score to 0-100 range
    exam_score = np.clip(exam_score, 0, 100)
    
    # 3. Generate Classification Target (grade)
    # A: >= 90, B: 80-89, C: 70-79, D: 60-69, F: <60
    grades = []
    for score in exam_score:
        if score >= 90:
            grades.append('A')
        elif score >= 80:
            grades.append('B')
        elif score >= 70:
            grades.append('C')
        elif score >= 60:
            grades.append('D')
        else:
            grades.append('F')
            
    # Create DataFrame
    df = pd.DataFrame({
        'study_hours_per_week': np.round(study_hours_per_week, 1),
        'attendance_percentage': np.round(attendance_percentage, 1),
        'previous_exam_score': np.round(previous_exam_score, 1),
        'assignments_completed': assignments_completed,
        'sleep_hours': np.round(sleep_hours, 1),
        'extracurricular_hours': np.round(extracurricular_hours, 1),
        'parent_education_level': parent_education_level,
        'internet_access': internet_access,
        'exam_score': np.round(exam_score, 1),
        'grade': grades
    })
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/student_data.csv', index=False)
    print(f"Generated {num_students} records and saved to data/student_data.csv")
    
if __name__ == "__main__":
    generate_student_data()
