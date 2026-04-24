import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, 
                             precision_score, recall_score, f1_score, 
                             classification_report)
import warnings
import json
warnings.filterwarnings('ignore')

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Model Training Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stProgress > div > div > div > div { background-color: #1f77b4; }
        h1 { color: #1f77b4; }
        h2 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# TITLE AND INTRODUCTION
# ============================================================================
st.title("🤖 Random Forest Model Training Dashboard")
st.markdown("### Customer Churn Prediction - Data Preprocessing & Model Training")

st.sidebar.header("⚙️ Training Configuration")

# ============================================================================
# STEP 1: DATA LOADING AND EXPLORATION
# ============================================================================
st.header("STEP 1: Data Loading and Exploration")

with st.spinner("Loading dataset..."):
    df = pd.read_csv('Customertravel.csv')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", df.shape[0])
with col2:
    st.metric("Total Features", df.shape[1])
with col3:
    st.metric("Missing Values", df.isnull().sum().sum())

st.subheader("📊 Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Data Info")
    st.write(df.dtypes)

with col2:
    st.subheader("Target Distribution")
    target_dist = df['Target'].value_counts()
    st.bar_chart(target_dist)

# Check for "No Record" values
no_record_count = (df['FrequentFlyer'] == 'No Record').sum()
st.info(f"✓ 'No Record' values found in FrequentFlyer: {no_record_count}")

# ============================================================================
# STEP 2: DATA PREPROCESSING
# ============================================================================
st.header("STEP 2: Data Preprocessing")

progress_bar = st.progress(0)

with st.spinner("Processing data..."):
    # Copy data
    data = df.copy()
    progress_bar.progress(20)
    
    # 2.1: Handle "No Record" values
    st.subheader("2.1 Handling 'No Record' Values")
    freq_flyer_mode = data[data['FrequentFlyer'] != 'No Record']['FrequentFlyer'].mode()[0]
    st.write(f"✓ Mode for FrequentFlyer: **{freq_flyer_mode}**")
    data['FrequentFlyer'] = data['FrequentFlyer'].replace('No Record', freq_flyer_mode)
    st.success(f"✓ 'No Record' values replaced with '{freq_flyer_mode}'")
    progress_bar.progress(30)
    
    # 2.2: Separate features and target
    st.subheader("2.2 Separating Features and Target")
    X = data.drop('Target', axis=1)
    y = data['Target']
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Features Shape", X.shape)
    with col2:
        st.metric("Target Shape", y.shape)
    progress_bar.progress(40)
    
    # 2.3: Identify categorical and numerical columns
    st.subheader("2.3 Feature Classification")
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Categorical Columns:**")
        st.write(categorical_cols)
    with col2:
        st.write("**Numerical Columns:**")
        st.write(numerical_cols)
    progress_bar.progress(50)
    
    # 2.4: Encode categorical features
    st.subheader("2.4 Encoding Categorical Features")
    label_encoders = {}
    
    encoding_info = []
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
        encoding_dict = dict(zip(le.classes_, le.transform(le.classes_)))
        encoding_info.append(f"**{col}**: {encoding_dict}")
    
    for info in encoding_info:
        st.write(info)
    
    st.write("**Data after encoding:**")
    st.dataframe(X.head(10), use_container_width=True)
    progress_bar.progress(60)
    
    # 2.5: Train-Test Split
    st.subheader("2.5 Train-Test Split")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Training Size", X_train.shape[0])
    with col2:
        st.metric("Testing Size", X_test.shape[0])
    with col3:
        st.metric("Train Churn %", f"{y_train.mean():.1%}")
    with col4:
        st.metric("Test Churn %", f"{y_test.mean():.1%}")
    
    progress_bar.progress(70)

st.success("✓ Data Preprocessing Complete!")


# ============================================================================
# STEP 3: MODEL TRAINING
# ============================================================================
st.header("STEP 3: Training Random Forest Classifier")

# Hyperparameter configuration in sidebar
st.sidebar.subheader("Random Forest Hyperparameters")
n_estimators = st.sidebar.slider("Number of Trees", min_value=50, max_value=300, value=100, step=10)
max_depth = st.sidebar.slider("Max Depth", min_value=5, max_value=30, value=15, step=1)
min_samples_split = st.sidebar.slider("Min Samples Split", min_value=2, max_value=20, value=10, step=1)
min_samples_leaf = st.sidebar.slider("Min Samples Leaf", min_value=1, max_value=10, value=4, step=1)

st.write(f"""
**Current Hyperparameters:**
- Number of Trees: {n_estimators}
- Max Depth: {max_depth}
- Min Samples Split: {min_samples_split}
- Min Samples Leaf: {min_samples_leaf}
""")

# Train button
if st.button("🚀 Train Model", use_container_width=True, type="primary"):
    with st.spinner("Training the Random Forest model..."):
        progress_bar = st.progress(0)
        
        rf_model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        rf_model.fit(X_train, y_train)
        progress_bar.progress(100)
        
        st.success("✓ Model training completed!")
        
        # ====================================================================
        # STEP 4: MODEL EVALUATION
        # ====================================================================
        st.header("STEP 4: Model Evaluation")
        
        # Predictions
        y_train_pred = rf_model.predict(X_train)
        y_test_pred = rf_model.predict(X_test)
        
        # Metrics
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        test_precision = precision_score(y_test, y_test_pred)
        test_recall = recall_score(y_test, y_test_pred)
        test_f1 = f1_score(y_test, y_test_pred)
        
        st.subheader("4.1 Accuracy Scores")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Training Accuracy", f"{train_accuracy:.4f}", delta=None)
        with col2:
            st.metric("Testing Accuracy", f"{test_accuracy:.4f}", delta=None)
        
        st.subheader("4.2 Test Set Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Accuracy", f"{test_accuracy:.4f}")
        with col2:
            st.metric("Precision", f"{test_precision:.4f}")
        with col3:
            st.metric("Recall", f"{test_recall:.4f}")
        with col4:
            st.metric("F1-Score", f"{test_f1:.4f}")
        
        # Confusion Matrix
        st.subheader("4.3 Confusion Matrix")
        cm = confusion_matrix(y_test, y_test_pred)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("True Negatives", cm[0, 0])
        with col2:
            st.metric("False Positives", cm[0, 1])
        with col3:
            st.metric("False Negatives", cm[1, 0])
        with col4:
            st.metric("True Positives", cm[1, 1])
        
        # Classification Report
        st.subheader("4.4 Detailed Classification Report")
        report = classification_report(y_test, y_test_pred, 
                                      target_names=['No Churn (0)', 'Churn (1)'],
                                      output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df, use_container_width=True)
        
        # ====================================================================
        # STEP 5: FEATURE IMPORTANCE
        # ====================================================================
        st.header("STEP 5: Feature Importance Analysis")
        
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        st.dataframe(feature_importance, use_container_width=True)
        
        # ====================================================================
        # STEP 6: VISUALIZATION
        # ====================================================================
        st.header("STEP 6: Generating Visualizations")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Confusion Matrix Heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0],
                    xticklabels=['No Churn', 'Churn'],
                    yticklabels=['No Churn', 'Churn'])
        axes[0, 0].set_title('Confusion Matrix', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('True Label')
        axes[0, 0].set_xlabel('Predicted Label')
        
        # Feature Importance Bar Chart
        axes[0, 1].barh(feature_importance['Feature'], feature_importance['Importance'], 
                        color='steelblue')
        axes[0, 1].set_xlabel('Importance Score', fontweight='bold')
        axes[0, 1].set_title('Feature Importance - Random Forest', fontsize=12, fontweight='bold')
        axes[0, 1].invert_yaxis()
        
        # Model Performance Metrics
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        scores = [test_accuracy, test_precision, test_recall, test_f1]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        axes[1, 0].bar(metrics, scores, color=colors, alpha=0.7)
        axes[1, 0].set_ylabel('Score', fontweight='bold')
        axes[1, 0].set_title('Model Performance Metrics', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylim([0, 1])
        axes[1, 0].axhline(y=test_accuracy, color='gray', linestyle='--', alpha=0.5)
        for i, v in enumerate(scores):
            axes[1, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
        
        # Class Distribution
        class_dist = y_test.value_counts()
        axes[1, 1].pie(class_dist, labels=['No Churn (0)', 'Churn (1)'], 
                       autopct='%1.1f%%', colors=['#90ee90', '#ff6b6b'], startangle=90)
        axes[1, 1].set_title('Test Set - Target Distribution', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('model_evaluation.png', dpi=300, bbox_inches='tight')
        st.pyplot(fig)
        st.success("✓ Visualization saved as 'model_evaluation.png'")
        
        # ====================================================================
        # STEP 7: SAVE MODEL AND ENCODERS
        # ====================================================================
        st.header("STEP 7: Saving Model and Preprocessors")
        
        model_artifacts = {
            'model': rf_model,
            'label_encoders': label_encoders,
            'feature_names': X.columns.tolist(),
            'categorical_cols': categorical_cols,
            'numerical_cols': numerical_cols
        }
        
        with open('model.pkl', 'wb') as f:
            pickle.dump(model_artifacts, f)
        st.success("✓ Model artifacts saved to 'model.pkl'")
        
        # Save metrics to JSON
        metrics_dict = {
            'accuracy': float(test_accuracy),
            'precision': float(test_precision),
            'recall': float(test_recall),
            'f1_score': float(test_f1),
            'confusion_matrix': cm.tolist(),
            'feature_importance': feature_importance.to_dict(orient='records')
        }
        
        with open('model_metrics.json', 'w') as f:
            json.dump(metrics_dict, f, indent=4)
        st.success("✓ Model metrics saved to 'model_metrics.json'")
        
        st.markdown("---")
        st.success("""
        ### 🎉 MODEL TRAINING COMPLETE!
        
        **Next Steps:**
        1. Your model is ready for deployment
        2. Use `app.py` with Streamlit to make predictions: `streamlit run app.py`
        3. Model files saved:
           - `model.pkl` - Trained model & encoders
           - `model_metrics.json` - Performance metrics
           - `model_evaluation.png` - Visualization charts
        """)
else:
    st.info("👈 Click the '🚀 Train Model' button to start training the Random Forest classifier")
