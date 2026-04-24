import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, 
                             precision_score, recall_score, f1_score, 
                             classification_report)
import warnings
import json
import os

warnings.filterwarnings('ignore')

def train():
    print("🤖 Starting Model Training Pipeline...")
    
    # 1. Load Data
    print("\n[1/5] Loading Data...")
    try:
        df = pd.read_csv('Customertravel.csv')
        print(f"Loaded {df.shape[0]} records with {df.shape[1]} features.")
    except FileNotFoundError:
        print("Error: Customertravel.csv not found!")
        return

    data = df.copy()

    # 2. Preprocess Data
    print("\n[2/5] Preprocessing Data...")
    freq_flyer_mode = data[data['FrequentFlyer'] != 'No Record']['FrequentFlyer'].mode()[0]
    data['FrequentFlyer'] = data['FrequentFlyer'].replace('No Record', freq_flyer_mode)
    
    X = data.drop('Target', axis=1)
    y = data['Target']
    
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Train Model
    print("\n[3/5] Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    rf_model.fit(X_train, y_train)

    # 4. Evaluate Model
    print("\n[4/5] Evaluating Model...")
    y_test_pred = rf_model.predict(X_test)
    
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred)
    test_recall = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    
    print(f"Accuracy: {test_accuracy:.4f}")
    print(f"Precision: {test_precision:.4f}")
    print(f"Recall: {test_recall:.4f}")
    print(f"F1-Score: {test_f1:.4f}")

    # 5. Save Artifacts
    print("\n[5/5] Saving Model Artifacts...")
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    model_artifacts = {
        'model': rf_model,
        'label_encoders': label_encoders,
        'feature_names': X.columns.tolist(),
        'categorical_cols': categorical_cols,
        'numerical_cols': numerical_cols
    }
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model_artifacts, f)
        
    metrics_dict = {
        'accuracy': float(test_accuracy),
        'precision': float(test_precision),
        'recall': float(test_recall),
        'f1_score': float(test_f1),
        'confusion_matrix': confusion_matrix(y_test, y_test_pred).tolist(),
        'feature_importance': feature_importance.to_dict(orient='records')
    }
    
    with open('model_metrics.json', 'w') as f:
        json.dump(metrics_dict, f, indent=4)
        
    print("\n✅ Training Complete! Artifacts saved to 'model.pkl' and 'model_metrics.json'.")

if __name__ == "__main__":
    train()
