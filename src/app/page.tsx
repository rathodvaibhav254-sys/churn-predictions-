"use client";
import { useState } from 'react';

export default function Home() {
  const [formData, setFormData] = useState({
    age: 35,
    freqFlyer: 'No',
    income: 'Middle Income',
    services: 3,
    social: 'No',
    hotel: 'No'
  });

  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<{ pred: number; prob: number } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (res.ok) {
        setPrediction({ pred: data.prediction, prob: data.probability });
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      console.error(error);
      alert('Failed to connect to prediction API');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' || name === 'services' ? Number(value) : value
    }));
  };

  return (
    <div className="min-h-screen bg-white">
      <main className="streamlit-container flex flex-col gap-8">
        <h1 className="text-4xl font-bold mb-4">🔮 Predict Churn</h1>
        
        <div className="flex flex-col md:flex-row gap-8">
          {/* Form Section */}
          <section className="flex-1">
            <h2 className="text-2xl font-semibold mb-4">📋 Customer Details</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block mb-1 text-sm">Age: {formData.age}</label>
                <input type="range" name="age" min="18" max="80" value={formData.age} onChange={handleChange} className="w-full" />
              </div>

              <div>
                <label className="block mb-1 text-sm">Frequent Flyer</label>
                <select name="freqFlyer" value={formData.freqFlyer} onChange={handleChange} className="st-input">
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>

              <div>
                <label className="block mb-1 text-sm">Income</label>
                <select name="income" value={formData.income} onChange={handleChange} className="st-input">
                  <option value="Low Income">Low Income</option>
                  <option value="Middle Income">Middle Income</option>
                  <option value="High Income">High Income</option>
                </select>
              </div>

              <div>
                <label className="block mb-1 text-sm">Services: {formData.services}</label>
                <input type="range" name="services" min="1" max="6" value={formData.services} onChange={handleChange} className="w-full" />
              </div>

              <div>
                <label className="block mb-1 text-sm">Social Media</label>
                <select name="social" value={formData.social} onChange={handleChange} className="st-input">
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>

              <div>
                <label className="block mb-1 text-sm">Hotel</label>
                <select name="hotel" value={formData.hotel} onChange={handleChange} className="st-input">
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>

              <button type="submit" disabled={loading} className="st-btn mt-4">
                {loading ? 'Processing...' : 'Predict'}
              </button>
            </form>
          </section>

          {/* Results Section */}
          <section className="flex-1">
            <h2 className="text-2xl font-semibold mb-4">🎲 Prediction Results</h2>
            
            {prediction && (
              <div className="space-y-6">
                <hr className="border-gray-200" />
                
                {/* Main Prediction Display matched to Streamlit app.py exactly */}
                {prediction.pred === 1 ? (
                  <div className="st-card-danger">
                    <h3 className="text-[#ff6b6b] mt-0 text-xl font-bold mb-2">⚠️ CUSTOMER WILL CHURN</h3>
                    <p className="text-[18px] text-[#ff6b6b] font-bold m-0">Churn Risk: {prediction.prob.toFixed(1)}%</p>
                  </div>
                ) : prediction.prob > 40 ? (
                  <div className="st-card-warn">
                    <h3 className="text-[#ff8c00] mt-0 text-xl font-bold mb-2">⚠️ CUSTOMER AT RISK</h3>
                    <p className="text-[18px] text-[#ff8c00] font-bold m-0">Churn Risk: {prediction.prob.toFixed(1)}%</p>
                  </div>
                ) : (
                  <div className="st-card-safe">
                    <h3 className="text-[#51cf66] mt-0 text-xl font-bold mb-2">✅ CUSTOMER WILL NOT CHURN</h3>
                    <p className="text-[18px] text-[#51cf66] font-bold m-0">Churn Risk: {prediction.prob.toFixed(1)}%</p>
                  </div>
                )}
                
                <hr className="border-gray-200" />
                
                <div>
                  <h3 className="text-xl font-semibold mb-4">📊 Probability Breakdown</h3>
                  <div className="flex gap-4">
                    <div className="flex-1 st-card text-center">
                      <p className="text-sm text-gray-600">No Churn Probability</p>
                      <p className="text-2xl font-mono">{(100 - prediction.prob).toFixed(2)}%</p>
                    </div>
                    <div className="flex-1 st-card text-center">
                      <p className="text-sm text-gray-600">Churn Probability</p>
                      <p className="text-2xl font-mono">{prediction.prob.toFixed(2)}%</p>
                    </div>
                  </div>
                </div>

                <hr className="border-gray-200" />
                
                <div>
                  <h3 className="text-xl font-semibold mb-4">🎯 Recommendation</h3>
                  {prediction.pred === 1 ? (
                    <>
                      <div className="bg-[#ffcccc] text-[#cc0000] p-3 rounded mb-2">🔴 <strong>Status:</strong> IMMEDIATE ACTION REQUIRED</div>
                      <div className="bg-[#fff3cd] text-[#856404] p-3 rounded">
                        <strong>Actions to take:</strong>
                        <ul className="list-disc ml-5 mt-1">
                          <li>Initiate retention campaign immediately</li>
                          <li>Offer personalized travel packages</li>
                          <li>Provide exclusive loyalty rewards</li>
                          <li>Schedule direct customer outreach</li>
                          <li>Review recent complaints or issues</li>
                        </ul>
                      </div>
                    </>
                  ) : prediction.prob > 40 ? (
                    <>
                      <div className="bg-[#fff3cd] text-[#856404] p-3 rounded mb-2">🟠 <strong>Status:</strong> MONITOR CLOSELY</div>
                      <div className="bg-[#d1ecf1] text-[#0c5460] p-3 rounded">
                        <strong>Actions to take:</strong>
                        <ul className="list-disc ml-5 mt-1">
                          <li>Monitor customer activity</li>
                          <li>Proactive engagement campaigns</li>
                          <li>Offer special incentives</li>
                          <li>Regular check-in calls</li>
                        </ul>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="bg-[#d4edda] text-[#155724] p-3 rounded mb-2">🟢 <strong>Status:</strong> SATISFIED CUSTOMER</div>
                      <div className="bg-[#d4edda] text-[#155724] p-3 rounded">
                        <strong>Actions to take:</strong>
                        <ul className="list-disc ml-5 mt-1">
                          <li>Continue excellent service</li>
                          <li>Encourage loyalty program participation</li>
                          <li>Upsell additional services</li>
                          <li>Request referrals</li>
                        </ul>
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}
          </section>
        </div>
        
        <hr className="border-gray-200 mt-8" />
        <div className="text-center text-[#888] text-[11px] pt-4">
          <p>🚀 Random Forest Churn Prediction | v1.0</p>
        </div>
      </main>
    </div>
  );
}
