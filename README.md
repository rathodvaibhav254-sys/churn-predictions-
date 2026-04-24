# Customer Churn Prediction using Random Forest

This project builds a Random Forest Classification model to predict customer churn in the travel industry.

## 📁 Project Structure

```
├── Customertravel.csv          # Raw dataset with customer attributes
├── train_model.py              # Training script - builds and evaluates the model
├── app.py                      # Streamlit web app - interactive prediction interface
├── model.pkl                   # Serialized trained model (generated after training)
├── model_metrics.json          # Model performance metrics (generated after training)
├── model_evaluation.png        # Visualizations (generated after training)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

Run the training script to preprocess data, train the Random Forest model, and generate evaluations:

```bash
python train_model.py
```

**What this script does:**
- ✅ Loads and explores the Customertravel.csv dataset
- ✅ Handles "No Record" values in categorical features
- ✅ Encodes categorical variables (FrequentFlyer, AnnualIncomeClass, etc.)
- ✅ Splits data into training (80%) and testing (20%) sets
- ✅ Trains a Random Forest Classifier with optimized hyperparameters
- ✅ Evaluates the model with Confusion Matrix, Accuracy, Precision, Recall, F1-Score
- ✅ Generates feature importance rankings
- ✅ Creates visualization charts (model_evaluation.png)
- ✅ Saves the model to model.pkl
- ✅ Saves metrics to model_metrics.json

**Output:**
- Console output with all training and evaluation metrics
- `model.pkl` - Trained model and preprocessing objects
- `model_metrics.json` - Performance metrics in JSON format
- `model_evaluation.png` - 4-panel visualization with confusion matrix, feature importance, metrics, and class distribution

### Step 3: Run the Streamlit App

Once the model is trained, launch the interactive web application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📊 Streamlit App Features

### 🔮 Make Prediction
- Input customer attributes (Age, Frequent Flyer status, Income class, etc.)
- Get instant churn risk probability
- Receive actionable recommendations based on risk level

### 📊 Model Performance
- View all evaluation metrics (Accuracy, Precision, Recall, F1-Score)
- Interactive Confusion Matrix visualization
- Detailed breakdown of true positives, true negatives, false positives, false negatives

### 📈 Feature Insights
- Feature importance ranking showing which attributes drive churn predictions
- Business insights for each feature in the travel context
- Explanation of how Random Forest uses these features to make decisions

## 🔄 Data Preprocessing Details

### Handling "No Record" Values
- Identified in the `FrequentFlyer` column
- **Strategy Used**: Mode imputation (replaced with most frequent value: "Yes" or "No")
- Alternative approaches: Deletion, separate category encoding

### Categorical Encoding
- **Method**: Label Encoding (converts categories to integers)
  - FrequentFlyer: No=0, Yes=1
  - AnnualIncomeClass: Low Income=0, Middle Income=1, High Income=2
  - AccountSyncedToSocialMedia: No=0, Yes=1
  - BookedHotelOrNot: No=0, Yes=1

### Train-Test Split
- 80% training set, 20% test set
- Stratified split maintains class distribution
- Prevents data leakage with separate preprocessing

## 🌳 Random Forest Model Details

### Hyperparameters Optimized
```python
n_estimators=100        # 100 decision trees in the ensemble
max_depth=15            # Maximum tree depth to prevent overfitting
min_samples_split=10    # Minimum samples required to split a node
min_samples_leaf=4      # Minimum samples required at leaf nodes
class_weight='balanced' # Handles imbalanced churn classes
```

### Why Random Forest for Travel Churn?

1. **Mixed Data Types**: Naturally handles numerical (Age, ServicesOpted) and categorical features
2. **Non-Linear Relationships**: Discovers complex patterns in travel behavior
3. **Feature Interactions**: Captures how features interact (e.g., young + low-income customers)
4. **Interpretability**: Feature importance shows which attributes matter most
5. **Robust**: Less sensitive to outliers and missing patterns
6. **Probability Estimates**: Provides churn probability for risk-based targeting

## 📈 Model Performance

Example output metrics:
- **Accuracy**: ~85-90% (overall correctness)
- **Precision**: ~80-85% (reliability when flagging churners)
- **Recall**: ~70-80% (catches most actual churners)
- **F1-Score**: ~75-85% (balanced precision-recall measure)

## 🎯 Business Applications

### 1. **Proactive Retention**
   - Identify high-risk customers before they leave
   - Prioritize retention campaigns

### 2. **Personalized Interventions**
   - Use feature importance to tailor retention offers
   - Focus on key behavioral factors (services, booking patterns)

### 3. **Revenue Protection**
   - Reduce customer acquisition costs by improving retention
   - Allocate resources to at-risk segments

### 4. **Customer Segmentation**
   - Identify churn risk groups (age + income + service combinations)
   - Create targeted loyalty programs

## 🔧 Customization & Enhancement

### Adjust Model Hyperparameters
Edit `train_model.py` line 89-96 to experiment with different settings:
```python
rf_model = RandomForestClassifier(
    n_estimators=150,      # Increase for more trees
    max_depth=20,          # Allow deeper trees
    min_samples_split=5,   # More flexible splitting
    # ... other parameters
)
```

### Add New Features
1. Add columns to Customertravel.csv
2. Update categorical_cols list in train_model.py if new feature is categorical
3. Re-run training

### Deploy to Cloud
- **Streamlit Cloud**: Free hosting at streamlit.io
- **Heroku**: Simple git-based deployment
- **AWS**: Use EC2 + Streamlit for enterprise deployments

## ❓ Troubleshooting

### Model files not found
```
Error: Model files not found! Please run 'train_model.py' first
Solution: Run python train_model.py before launching the app
```

### Port already in use
```
Solution: streamlit run app.py --server.port 8502
```

### Encoding errors on new data
- Ensure categorical values match training data exactly
- Check for extra whitespace or case differences
- The app uses the saved LabelEncoders from model.pkl

## 📚 Files Overview

| File | Purpose |
|------|---------|
| `train_model.py` | Data preprocessing, model training, evaluation, visualization |
| `app.py` | Interactive Streamlit web application for predictions |
| `model.pkl` | Serialized model, encoders, and preprocessing objects |
| `model_metrics.json` | Performance metrics and confusion matrix |
| `requirements.txt` | Python package dependencies |

## 🛠️ Requirements

- Python 3.8+
- See requirements.txt for library versions

## 📝 License

This project is provided as-is for educational and business purposes.

---

**Questions?** Review the comments in train_model.py and app.py for detailed explanations of each code section.
