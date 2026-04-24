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
    <div className="min-h-screen bg-slate-50">
      {/* Professional Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
              C
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-800 tracking-tight">ChurnPredict</h1>
              <p className="text-xs text-slate-500 font-medium">Enterprise Intelligence</p>
            </div>
          </div>
          <div className="text-sm text-slate-500 font-medium hidden sm:block">
            Model Status: <span className="text-green-600">Online</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-800">Customer Risk Assessment</h2>
          <p className="text-slate-500 mt-1">Enter customer demographics and behavior metrics to forecast retention.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Form Section */}
          <section className="lg:col-span-5">
            <div className="prof-card p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-5 border-b border-slate-100 pb-3">
                Customer Profile
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <div className="flex justify-between mb-1">
                    <label className="text-sm font-semibold text-slate-700">Age</label>
                    <span className="text-sm font-medium text-slate-500">{formData.age} years</span>
                  </div>
                  <input type="range" name="age" min="18" max="80" value={formData.age} onChange={handleChange} className="w-full accent-blue-600" />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Frequent Flyer Status</label>
                  <select name="freqFlyer" value={formData.freqFlyer} onChange={handleChange} className="prof-input">
                    <option value="Yes">Yes - Active</option>
                    <option value="No">No - Inactive</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Annual Income Bracket</label>
                  <select name="income" value={formData.income} onChange={handleChange} className="prof-input">
                    <option value="Low Income">Low Income</option>
                    <option value="Middle Income">Middle Income</option>
                    <option value="High Income">High Income</option>
                  </select>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <label className="text-sm font-semibold text-slate-700">Services Opted</label>
                    <span className="text-sm font-medium text-slate-500">{formData.services} services</span>
                  </div>
                  <input type="range" name="services" min="1" max="6" value={formData.services} onChange={handleChange} className="w-full accent-blue-600" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Social Media Sync</label>
                    <select name="social" value={formData.social} onChange={handleChange} className="prof-input">
                      <option value="Yes">Synced</option>
                      <option value="No">Not Synced</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Hotel Booked</label>
                    <select name="hotel" value={formData.hotel} onChange={handleChange} className="prof-input">
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>
                </div>

                <div className="pt-4 mt-2 border-t border-slate-100">
                  <button type="submit" disabled={loading} className="w-full prof-btn flex justify-center items-center gap-2">
                    {loading ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Running Analysis...
                      </>
                    ) : 'Run Prediction Model'}
                  </button>
                </div>
              </form>
            </div>
          </section>

          {/* Results Section */}
          <section className="lg:col-span-7">
            <div className="prof-card p-6 h-full flex flex-col">
              <h3 className="text-lg font-semibold text-slate-800 mb-5 border-b border-slate-100 pb-3">
                Analysis Results
              </h3>
              
              {!prediction ? (
                <div className="flex-1 flex flex-col items-center justify-center text-slate-400 p-12 text-center border-2 border-dashed border-slate-200 rounded-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mb-4 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <p className="font-medium text-slate-500">Awaiting input data</p>
                  <p className="text-sm mt-1">Submit the customer profile to generate a risk forecast.</p>
                </div>
              ) : (
                <div className="space-y-6 flex-1">
                  
                  {/* Status Banner */}
                  {prediction.pred === 1 ? (
                    <div className="status-danger p-5 rounded-lg flex items-center justify-between">
                      <div>
                        <h4 className="text-red-700 font-bold text-lg mb-1">High Churn Risk Detected</h4>
                        <p className="text-red-600 text-sm font-medium">Customer is highly likely to leave the platform.</p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-black text-red-700">{prediction.prob.toFixed(1)}%</div>
                        <div className="text-xs text-red-500 font-bold uppercase tracking-wider mt-1">Probability</div>
                      </div>
                    </div>
                  ) : prediction.prob > 40 ? (
                    <div className="status-warn p-5 rounded-lg flex items-center justify-between">
                      <div>
                        <h4 className="text-amber-700 font-bold text-lg mb-1">Elevated Risk Warning</h4>
                        <p className="text-amber-600 text-sm font-medium">Customer shows signs of potential churn.</p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-black text-amber-700">{prediction.prob.toFixed(1)}%</div>
                        <div className="text-xs text-amber-500 font-bold uppercase tracking-wider mt-1">Probability</div>
                      </div>
                    </div>
                  ) : (
                    <div className="status-safe p-5 rounded-lg flex items-center justify-between">
                      <div>
                        <h4 className="text-green-700 font-bold text-lg mb-1">Customer Retained</h4>
                        <p className="text-green-600 text-sm font-medium">Low risk of churn based on current metrics.</p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-black text-green-700">{prediction.prob.toFixed(1)}%</div>
                        <div className="text-xs text-green-500 font-bold uppercase tracking-wider mt-1">Probability</div>
                      </div>
                    </div>
                  )}
                  
                  {/* Probability Breakdown */}
                  <div>
                    <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3">Model Confidence</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-slate-50 border border-slate-200 p-4 rounded-lg">
                        <p className="text-xs text-slate-500 font-semibold mb-1 uppercase">Retention</p>
                        <div className="flex items-end gap-2">
                          <span className="text-2xl font-bold text-slate-800">{(100 - prediction.prob).toFixed(1)}</span>
                          <span className="text-slate-500 font-medium mb-1">%</span>
                        </div>
                      </div>
                      <div className="bg-slate-50 border border-slate-200 p-4 rounded-lg">
                        <p className="text-xs text-slate-500 font-semibold mb-1 uppercase">Attrition</p>
                        <div className="flex items-end gap-2">
                          <span className="text-2xl font-bold text-slate-800">{prediction.prob.toFixed(1)}</span>
                          <span className="text-slate-500 font-medium mb-1">%</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Actionable Insights */}
                  <div>
                    <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3">Recommended Actions</h4>
                    
                    <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
                      {prediction.pred === 1 ? (
                        <ul className="divide-y divide-slate-100">
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-red-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Deploy immediate retention offer via account manager.</span>
                          </li>
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-red-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Review recent support tickets for unresolved issues.</span>
                          </li>
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-red-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Offer personalized travel package discounts.</span>
                          </li>
                        </ul>
                      ) : prediction.prob > 40 ? (
                        <ul className="divide-y divide-slate-100">
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-amber-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Schedule a proactive check-in call within 7 days.</span>
                          </li>
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-amber-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Send targeted marketing campaigns based on activity.</span>
                          </li>
                        </ul>
                      ) : (
                        <ul className="divide-y divide-slate-100">
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-green-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Identify for upselling premium services.</span>
                          </li>
                          <li className="px-4 py-3 flex gap-3 items-start">
                            <span className="text-green-500 mt-0.5">•</span>
                            <span className="text-slate-700 text-sm">Request referral or testimonial.</span>
                          </li>
                        </ul>
                      )}
                    </div>
                  </div>

                </div>
              )}
            </div>
          </section>

        </div>
      </main>
      
      <footer className="mt-12 py-6 text-center border-t border-slate-200">
        <p className="text-slate-400 text-xs font-medium tracking-wide">
          © {new Date().getFullYear()} ChurnPredict ML Platform &middot; All rights reserved.
        </p>
      </footer>
    </div>
  );
}
