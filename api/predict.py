from http.server import BaseHTTPRequestHandler
import json
import pickle
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

# Load model and encoders once when the serverless function cold starts
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        artifacts = pickle.load(f)
        model = artifacts['model']
        label_encoders = artifacts['label_encoders']
        feature_names = artifacts['feature_names']
        categorical_cols = artifacts['categorical_cols']
except Exception as e:
    model = None
    print("Error loading model:", e)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if not model:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Model not loaded'}).encode())
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract inputs matching the Streamlit app logic
            input_data = pd.DataFrame({
                'Age': [data.get('age', 35)],
                'FrequentFlyer': [data.get('freqFlyer', 'No')],
                'AnnualIncomeClass': [data.get('income', 'Middle Income')],
                'ServicesOpted': [data.get('services', 3)],
                'AccountSyncedToSocialMedia': [data.get('social', 'No')],
                'BookedHotelOrNot': [data.get('hotel', 'No')]
            })
            
            # Encode categoricals
            input_enc = input_data.copy()
            for col in categorical_cols:
                if col in input_enc.columns:
                    le = label_encoders.get(col)
                    if le:
                        # Handle unseen labels by defaulting to 0 or similar, but for simplicity:
                        input_enc[col] = le.transform(input_data[col])
            
            # Reorder columns to match training
            input_enc = input_enc[feature_names]
            
            # Predict
            pred = model.predict(input_enc)[0]
            proba = model.predict_proba(input_enc)[0]
            churn_prob = proba[1] * 100
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'prediction': int(pred),
                'probability': float(churn_prob)
            }).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
