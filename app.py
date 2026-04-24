import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, 
                             precision_score, recall_score, f1_score, 
                             classification_report)
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(page_title="⚡ Churn Prediction", page_icon="⚡", layout="wide")

NEON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* ── Dark background ── */
.stApp {
    background: #0a0a0f !important;
    color: #e0e0e0 !important;
}
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
}

/* ── Animated neon gradient header bar ── */
.stApp > header {
    background: linear-gradient(90deg, #ff00ff33, #00ffff33, #ff00ff33) !important;
    background-size: 200% 100% !important;
    animation: headerGlow 4s ease infinite !important;
}
@keyframes headerGlow {
    0%,100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #1a0a2e 50%, #0d0d1a 100%) !important;
    border-right: 1px solid #ff00ff44 !important;
    box-shadow: 4px 0 25px #ff00ff22 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    color: #e0e0ff !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #c0c0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #00ffff !important;
    text-shadow: 0 0 8px #00ffff88 !important;
}

/* ── Headings ── */
h1, .stTitle {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, #ff00ff, #00ffff, #ff00ff) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: neonText 3s linear infinite !important;
    text-align: center !important;
    font-size: 2.2rem !important;
    letter-spacing: 2px !important;
}
@keyframes neonText {
    0%,100% { background-position: 0% center; }
    50% { background-position: 200% center; }
}
h2, h3, .stSubheader {
    font-family: 'Rajdhani', sans-serif !important;
    color: #00ffff !important;
    text-shadow: 0 0 10px #00ffff44 !important;
    border-bottom: 1px solid #00ffff22 !important;
    padding-bottom: 8px !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    border: 1px solid #00ffff33 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    box-shadow: 0 0 20px #00ffff11, inset 0 0 20px #00ffff05 !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: #ff00ff88 !important;
    box-shadow: 0 0 30px #ff00ff22, inset 0 0 30px #ff00ff08 !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] {
    color: #00ffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Orbitron', monospace !important;
    text-shadow: 0 0 10px #ff00ff44 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ff00ff, #8b00ff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 14px 28px !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 25px #ff00ff44, 0 0 50px #ff00ff22 !important;
    transition: all 0.3s ease !important;
    animation: btnPulse 2s ease-in-out infinite !important;
}
@keyframes btnPulse {
    0%,100% { box-shadow: 0 0 25px #ff00ff44, 0 0 50px #ff00ff22; }
    50% { box-shadow: 0 0 35px #ff00ff66, 0 0 70px #ff00ff33; }
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00ffff, #0088ff) !important;
    box-shadow: 0 0 35px #00ffff55, 0 0 70px #00ffff33 !important;
    transform: scale(1.03) !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] {
    background: transparent !important;
}
.stSlider [role="slider"] {
    background: #ff00ff !important;
    box-shadow: 0 0 12px #ff00ff88 !important;
}
.stSlider label {
    color: #c0c0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500 !important;
}

/* ── Select boxes ── */
.stSelectbox label, .stMultiSelect label {
    color: #c0c0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stSelectbox [data-baseweb="select"] {
    background: #1a1a2e !important;
    border: 1px solid #ff00ff44 !important;
    border-radius: 10px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #00ffff22 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Alert boxes ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid #00ffff33 !important;
}

/* ── Dividers ── */
hr {
    border-color: #ff00ff33 !important;
    box-shadow: 0 0 8px #ff00ff22 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #ff00ff !important;
}

/* ── Custom neon card class ── */
.neon-card {
    background: linear-gradient(135deg, #1a1a2ecc, #16213ecc) !important;
    border: 1px solid #00ffff33;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 0 20px #00ffff11;
    backdrop-filter: blur(10px);
}
.neon-card-danger {
    background: linear-gradient(135deg, #2e1a1acc, #3e1616cc) !important;
    border: 1px solid #ff006644;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 0 25px #ff006622;
    animation: dangerPulse 2s ease-in-out infinite;
}
@keyframes dangerPulse {
    0%,100% { box-shadow: 0 0 25px #ff006622; }
    50% { box-shadow: 0 0 40px #ff006644; }
}
.neon-card-safe {
    background: linear-gradient(135deg, #1a2e1acc, #163e16cc) !important;
    border: 1px solid #00ff6644;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 0 25px #00ff6622;
}
.neon-card-warn {
    background: linear-gradient(135deg, #2e2a1acc, #3e3016cc) !important;
    border: 1px solid #ffaa0044;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 0 25px #ffaa0022;
}

.neon-title { font-family: 'Orbitron', monospace; font-size: 22px; font-weight: 700; margin: 0 0 8px 0; }
.neon-value { font-family: 'Orbitron', monospace; font-size: 32px; font-weight: 900; margin: 0; }
.glow-magenta { color: #ff00ff; text-shadow: 0 0 15px #ff00ff88, 0 0 30px #ff00ff44; }
.glow-cyan { color: #00ffff; text-shadow: 0 0 15px #00ffff88, 0 0 30px #00ffff44; }
.glow-green { color: #00ff66; text-shadow: 0 0 15px #00ff6688, 0 0 30px #00ff6644; }
.glow-red { color: #ff0066; text-shadow: 0 0 15px #ff006688, 0 0 30px #ff006644; }
.glow-orange { color: #ffaa00; text-shadow: 0 0 15px #ffaa0088, 0 0 30px #ffaa0044; }

/* ── Footer ── */
.neon-footer {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: #ff00ff88;
    text-shadow: 0 0 8px #ff00ff44;
    padding: 20px 0;
    letter-spacing: 3px;
}

/* risk classes */
.risk-high { color: #ff0066; font-weight: bold; font-size: 20px; text-shadow: 0 0 10px #ff006688; }
.risk-low { color: #00ff66; font-weight: bold; font-size: 20px; text-shadow: 0 0 10px #00ff6688; }
.risk-medium { color: #ffaa00; font-weight: bold; font-size: 20px; text-shadow: 0 0 10px #ffaa0088; }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'rf_model' not in st.session_state:
    st.session_state.rf_model = None
if 'label_encoders' not in st.session_state:
    st.session_state.label_encoders = {}
if 'feature_names' not in st.session_state:
    st.session_state.feature_names = []
if 'categorical_cols' not in st.session_state:
    st.session_state.categorical_cols = []
if 'X_test' not in st.session_state:
    st.session_state.X_test = None
if 'y_test' not in st.session_state:
    st.session_state.y_test = None
if 'metrics_data' not in st.session_state:
    st.session_state.metrics_data = None

# ============================================================================
# AUTO-LOAD MODEL FROM SAVED FILES
# ============================================================================
import os

def load_saved_model():
    """Load model from saved files if they exist"""
    if os.path.exists('model.pkl') and os.path.exists('model_metrics.json'):
        try:
            with open('model.pkl', 'rb') as f:
                artifacts = pickle.load(f)
            with open('model_metrics.json', 'r') as f:
                metrics = json.load(f)
            
            st.session_state.rf_model = artifacts['model']
            st.session_state.label_encoders = artifacts['label_encoders']
            st.session_state.feature_names = artifacts['feature_names']
            st.session_state.categorical_cols = artifacts['categorical_cols']
            st.session_state.metrics_data = metrics
            st.session_state.model_trained = True
            return True
        except Exception as e:
            return False
    return False

# Auto-load model on app start
if not st.session_state.model_trained:
    load_saved_model()

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.markdown("<h1 style='font-family: Orbitron, monospace; text-align: center; color: #ff00ff; text-shadow: 0 0 20px #ff00ff88, 0 0 40px #ff00ff44; font-size: 1.4rem; letter-spacing: 2px;'>⚡ CHURN<br>PREDICTION</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#00ffff88; font-family:Rajdhani,sans-serif; font-size:12px; letter-spacing:3px;'>NEURAL ENGINE v2.0</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("⚡ NAVIGATION", ["📊 Train Model", "🔮 Predict", "📈 Performance"])

# ============================================================================
# PAGE 1: TRAIN MODEL
# ============================================================================
if page == "📊 Train Model":
    st.title("⚡ NEURAL FOREST TRAINING ⚡")
    
    try:
        # Load data
        df = pd.read_csv('Customertravel.csv')
        
        st.subheader("📊 Step 1: Data Exploration")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Records", str(df.shape[0]))
        with col2:
            st.metric("Features", str(df.shape[1]))
        with col3:
            st.metric("Missing", str(df.isnull().sum().sum()))
        
        st.dataframe(df.head(10), width='stretch')
        
        st.subheader("📊 Step 2: Data Preprocessing")
        
        with st.spinner("Processing..."):
            data = df.copy()
            
            # Handle No Record
            freq_flyer_mode = data[data['FrequentFlyer'] != 'No Record']['FrequentFlyer'].mode()[0]
            data['FrequentFlyer'] = data['FrequentFlyer'].replace('No Record', freq_flyer_mode)
            st.write(f"✓ Replaced 'No Record' with '{freq_flyer_mode}'")
            
            # Separate features
            X = data.drop('Target', axis=1)
            y = data['Target']
            st.write(f"✓ Features: {X.shape[0]} rows × {X.shape[1]} columns")
            st.write(f"✓ Target: {y.shape[0]} values")
            
            # Identify column types
            categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
            numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Categorical:**", categorical_cols)
            with col2:
                st.write("**Numerical:**", numerical_cols)
            
            # Encode
            label_encoders = {}
            for col in categorical_cols:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
                label_encoders[col] = le
            
            st.write("✓ Categorical features encoded")
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            st.write(f"✓ Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")
            
            # Store in session
            st.session_state.X_test = X_test
            st.session_state.y_test = y_test
            st.session_state.label_encoders = label_encoders
            st.session_state.feature_names = X.columns.tolist()
            st.session_state.categorical_cols = categorical_cols
            st.session_state.X_train = X_train
            st.session_state.y_train = y_train
        
        # Hyperparameters
        st.subheader("⚙️ Step 3: Hyperparameters")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            n_est = st.slider("Trees", 50, 300, 100)
        with col2:
            depth = st.slider("Max Depth", 5, 30, 15)
        with col3:
            split = st.slider("Min Split", 2, 20, 10)
        with col4:
            leaf = st.slider("Min Leaf", 1, 10, 4)
        
        if st.button("🚀 Train Model", type="primary", use_container_width=True):
            with st.spinner("Training..."):
                # Train
                rf = RandomForestClassifier(
                    n_estimators=n_est, max_depth=depth,
                    min_samples_split=split, min_samples_leaf=leaf,
                    random_state=42, n_jobs=-1, class_weight='balanced'
                )
                rf.fit(st.session_state.X_train, st.session_state.y_train)
                
                # Predictions
                y_pred = rf.predict(st.session_state.X_test)
                
                # Metrics
                acc = accuracy_score(st.session_state.y_test, y_pred)
                prec = precision_score(st.session_state.y_test, y_pred)
                rec = recall_score(st.session_state.y_test, y_pred)
                f1 = f1_score(st.session_state.y_test, y_pred)
                cm = confusion_matrix(st.session_state.y_test, y_pred)
                feat_imp = pd.DataFrame({
                    'Feature': st.session_state.feature_names,
                    'Importance': rf.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                # Save
                st.session_state.rf_model = rf
                st.session_state.model_trained = True
                st.session_state.metrics_data = {
                    'accuracy': float(acc),
                    'precision': float(prec),
                    'recall': float(rec),
                    'f1_score': float(f1),
                    'confusion_matrix': cm.tolist(),
                    'feature_importance': feat_imp.to_dict(orient='records')
                }
                
                # Save to files
                with open('model.pkl', 'wb') as f:
                    pickle.dump({
                        'model': rf, 'label_encoders': st.session_state.label_encoders,
                        'feature_names': st.session_state.feature_names,
                        'categorical_cols': st.session_state.categorical_cols,
                        'numerical_cols': numerical_cols
                    }, f)
                
                with open('model_metrics.json', 'w') as f:
                    json.dump(st.session_state.metrics_data, f, indent=4)
                
                st.success("✅ Model trained and saved!")
                
                # Show results
                st.subheader("📊 Results")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Accuracy", f"{acc:.4f}")
                with col2:
                    st.metric("Precision", f"{prec:.4f}")
                with col3:
                    st.metric("Recall", f"{rec:.4f}")
                with col4:
                    st.metric("F1-Score", f"{f1:.4f}")
                
                # Visualizations — neon dark theme
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                fig.patch.set_facecolor('#0a0a0f')
                for ax in axes.flat:
                    ax.set_facecolor('#0d0d1a')
                    ax.tick_params(colors='#c0c0ff')
                    ax.xaxis.label.set_color('#00ffff')
                    ax.yaxis.label.set_color('#00ffff')
                    ax.title.set_color('#ff00ff')
                    for spine in ax.spines.values():
                        spine.set_color('#ff00ff44')
                
                # Confusion Matrix — magenta/cyan cmap
                from matplotlib.colors import LinearSegmentedColormap
                neon_cmap = LinearSegmentedColormap.from_list('neon', ['#0d0d1a', '#1a0a2e', '#8b00ff', '#ff00ff'])
                sns.heatmap(cm, annot=True, fmt='d', cmap=neon_cmap, ax=axes[0, 0],
                            xticklabels=['No Churn', 'Churn'],
                            yticklabels=['No Churn', 'Churn'],
                            annot_kws={'color': '#00ffff', 'fontsize': 14, 'fontweight': 'bold'},
                            linewidths=2, linecolor='#ff00ff44')
                axes[0, 0].set_title('⚡ Confusion Matrix', fontsize=14, fontweight='bold')
                
                # Feature Importance — neon bars
                colors_fi = ['#ff00ff', '#cc00ff', '#aa00ff', '#8800ff', '#6600ff', '#4400ff']
                axes[0, 1].barh(feat_imp['Feature'], feat_imp['Importance'],
                               color=colors_fi[:len(feat_imp)], edgecolor='#ff00ff44')
                axes[0, 1].set_title('⚡ Feature Importance', fontsize=14, fontweight='bold')
                axes[0, 1].invert_yaxis()
                
                # Performance — neon bar colors
                metrics = ['Accuracy', 'Precision', 'Recall', 'F1']
                scores = [acc, prec, rec, f1]
                neon_colors = ['#00ffff', '#ff00ff', '#00ff66', '#ffaa00']
                bars = axes[1, 0].bar(metrics, scores, color=neon_colors, edgecolor='#ffffff22')
                axes[1, 0].set_title('⚡ Performance Metrics', fontsize=14, fontweight='bold')
                axes[1, 0].set_ylim([0, 1])
                for bar, score in zip(bars, scores):
                    axes[1, 0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                                   f'{score:.3f}', ha='center', color='#ffffff', fontweight='bold')
                
                # Distribution — neon pie
                dist = st.session_state.y_test.value_counts()
                wedge_colors = ['#00ff66', '#ff0066']
                axes[1, 1].pie(dist, labels=['No Churn', 'Churn'], autopct='%1.1f%%',
                              colors=wedge_colors, textprops={'color': '#e0e0e0', 'fontweight': 'bold'},
                              wedgeprops={'edgecolor': '#0a0a0f', 'linewidth': 2})
                axes[1, 1].set_title('⚡ Test Distribution', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
    
    except FileNotFoundError:
        st.error("❌ Customertravel.csv not found!")

# ============================================================================
# PAGE 2: PREDICT
# ============================================================================
elif page == "🔮 Predict":
    st.title("⚡ CHURN ORACLE ⚡")
    
    # Check if model is loaded
    if st.session_state.model_trained:
        st.success("✅ Model loaded successfully!")
    else:
        st.error("❌ Model not trained yet!")
    
    if not st.session_state.model_trained:
        st.warning("⚠️ Please train the model first on the '📊 Train Model' page")
    else:
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.subheader("📋 Customer Details")
            age = st.slider("Age", 18, 80, 35)
            freq = st.selectbox("Frequent Flyer", ["Yes", "No"])
            income = st.selectbox("Income", ["Low Income", "Middle Income", "High Income"])
            services = st.slider("Services", 1, 6, 3)
            social = st.selectbox("Social Media", ["Yes", "No"])
            hotel = st.selectbox("Hotel", ["Yes", "No"])
        
        with col2:
            st.subheader("🎲 Prediction Results")
            
            input_data = pd.DataFrame({
                'Age': [age], 'FrequentFlyer': [freq],
                'AnnualIncomeClass': [income], 'ServicesOpted': [services],
                'AccountSyncedToSocialMedia': [social], 'BookedHotelOrNot': [hotel]
            })
            
            input_enc = input_data.copy()
            for col in st.session_state.categorical_cols:
                input_enc[col] = st.session_state.label_encoders[col].transform(input_data[col])
            
            input_enc = input_enc[st.session_state.feature_names]
            
            pred = st.session_state.rf_model.predict(input_enc)[0]
            proba = st.session_state.rf_model.predict_proba(input_enc)[0]
            churn_prob = proba[1] * 100
            
            st.markdown("---")
            
            # Main Prediction Display — neon cards
            if pred == 1:
                st.markdown(f"<div class='neon-card-danger'><p class='neon-title glow-red'>🚨 CUSTOMER WILL CHURN</p><p class='neon-value glow-red'>{churn_prob:.1f}%</p><p style='color:#ff006688; font-family:Rajdhani,sans-serif; margin:4px 0 0;'>THREAT LEVEL: CRITICAL</p></div>", unsafe_allow_html=True)
            elif churn_prob > 40:
                st.markdown(f"<div class='neon-card-warn'><p class='neon-title glow-orange'>⚠️ CUSTOMER AT RISK</p><p class='neon-value glow-orange'>{churn_prob:.1f}%</p><p style='color:#ffaa0088; font-family:Rajdhani,sans-serif; margin:4px 0 0;'>THREAT LEVEL: ELEVATED</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='neon-card-safe'><p class='neon-title glow-green'>✅ CUSTOMER SECURE</p><p class='neon-value glow-green'>{churn_prob:.1f}%</p><p style='color:#00ff6688; font-family:Rajdhani,sans-serif; margin:4px 0 0;'>THREAT LEVEL: MINIMAL</p></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Probability Breakdown
            st.subheader("📊 Probability Breakdown")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("No Churn Probability", f"{proba[0]*100:.2f}%")
            with col_b:
                st.metric("Churn Probability", f"{proba[1]*100:.2f}%")
            
            st.markdown("---")
            
            # Recommendation
            st.subheader("🎯 Recommendation")
            if pred == 1:
                st.error("🔴 **Status:** IMMEDIATE ACTION REQUIRED")
                st.warning("""
                **Actions to take:**
                - Initiate retention campaign immediately
                - Offer personalized travel packages
                - Provide exclusive loyalty rewards
                - Schedule direct customer outreach
                - Review recent complaints or issues
                """)
            elif churn_prob > 40:
                st.warning("🟠 **Status:** MONITOR CLOSELY")
                st.info("""
                **Actions to take:**
                - Monitor customer activity
                - Proactive engagement campaigns
                - Offer special incentives
                - Regular check-in calls
                """)
            else:
                st.success("🟢 **Status:** SATISFIED CUSTOMER")
                st.success("""
                **Actions to take:**
                - Continue excellent service
                - Encourage loyalty program participation
                - Upsell additional services
                - Request referrals
                """)

# ============================================================================
# PAGE 3: PERFORMANCE
# ============================================================================
elif page == "📈 Performance":
    st.title("⚡ SYSTEM DIAGNOSTICS ⚡")
    
    if not st.session_state.model_trained:
        st.warning("⚠️ Train model first on 'Train Model' page")
    else:
        if st.session_state.metrics_data is None:
            try:
                with open('model_metrics.json', 'r') as f:
                    st.session_state.metrics_data = json.load(f)
            except FileNotFoundError:
                st.error("Metrics file not found")
                st.stop()
        
        metrics = st.session_state.metrics_data
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Accuracy", f"{metrics['accuracy']:.4f}")
        with col2:
            st.metric("Precision", f"{metrics['precision']:.4f}")
        with col3:
            st.metric("Recall", f"{metrics['recall']:.4f}")
        with col4:
            st.metric("F1-Score", f"{metrics['f1_score']:.4f}")
        
        st.markdown("---")
        
        # Confusion Matrix — neon style
        st.subheader("⚡ Confusion Matrix")
        cm = np.array(metrics['confusion_matrix'])
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#0a0a0f')
        ax.set_facecolor('#0d0d1a')
        from matplotlib.colors import LinearSegmentedColormap
        neon_cmap2 = LinearSegmentedColormap.from_list('neon2', ['#0d0d1a', '#1a0a2e', '#8b00ff', '#ff00ff'])
        sns.heatmap(cm, annot=True, fmt='d', cmap=neon_cmap2, ax=ax,
                   xticklabels=['No Churn', 'Churn'],
                   yticklabels=['No Churn', 'Churn'],
                   annot_kws={'color': '#00ffff', 'fontsize': 16, 'fontweight': 'bold'},
                   linewidths=2, linecolor='#ff00ff44')
        ax.set_ylabel('True Label', color='#00ffff')
        ax.set_xlabel('Predicted Label', color='#00ffff')
        ax.tick_params(colors='#c0c0ff')
        ax.title.set_color('#ff00ff')
        for spine in ax.spines.values():
            spine.set_color('#ff00ff44')
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='neon-card'><span class='glow-green'>TN: {int(cm[0,0])}</span> &nbsp;|&nbsp; <span class='glow-red'>FP: {int(cm[0,1])}</span></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='neon-card'><span class='glow-red'>FN: {int(cm[1,0])}</span> &nbsp;|&nbsp; <span class='glow-green'>TP: {int(cm[1,1])}</span></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feature Importance — neon style
        st.subheader("⚡ Feature Importance")
        feat_df = pd.DataFrame(metrics['feature_importance']).sort_values('Importance', ascending=False)
        st.dataframe(feat_df, width='stretch')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#0a0a0f')
        ax.set_facecolor('#0d0d1a')
        neon_bar_colors = ['#ff00ff', '#cc00ff', '#aa00ff', '#8800ff', '#6600ff', '#4400ff', '#2200ff', '#0044ff']
        ax.barh(feat_df['Feature'], feat_df['Importance'],
                color=neon_bar_colors[:len(feat_df)], edgecolor='#ff00ff44')
        ax.set_xlabel('Importance', color='#00ffff')
        ax.set_title('⚡ Feature Importance', color='#ff00ff', fontsize=14, fontweight='bold')
        ax.tick_params(colors='#c0c0ff')
        for spine in ax.spines.values():
            spine.set_color('#ff00ff44')
        ax.invert_yaxis()
        st.pyplot(fig)

st.markdown("---")
st.markdown("<div class='neon-footer'>⚡ NEURAL CHURN ENGINE v2.0 ⚡<br><span style='font-size:9px; color:#00ffff44;'>POWERED BY RANDOM FOREST CLASSIFIER</span></div>", unsafe_allow_html=True)
