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
    <div className="min-h-screen bg-[#e9eaec] pb-12">
      
      {/* Top Floating Nav Bar */}
      <div className="pt-4 px-4 max-w-[1400px] mx-auto">
        <nav className="nav-bar px-2 py-2 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="pl-4">
              {/* Logo / Icon */}
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="#faff00" stroke="#faff00" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="flex space-x-1">
              <div className="bg-white text-black px-6 py-2 rounded-full font-bold text-sm">Predict</div>
              <div className="text-gray-400 hover:text-white px-4 py-2 rounded-full font-medium text-sm cursor-pointer transition-colors">Performance</div>
              <div className="text-gray-400 hover:text-white px-4 py-2 rounded-full font-medium text-sm cursor-pointer transition-colors">Customers</div>
              <div className="text-gray-400 hover:text-white px-4 py-2 rounded-full font-medium text-sm cursor-pointer transition-colors">Data</div>
            </div>
          </div>
          <div className="flex items-center gap-3 pr-2">
            <div className="w-8 h-8 rounded-full border border-gray-600 flex items-center justify-center text-gray-300">
              <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <div className="w-8 h-8 rounded-full border border-gray-600 flex items-center justify-center text-gray-300">
              <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            </div>
            <div className="w-8 h-8 rounded-full bg-gray-500 overflow-hidden border-2 border-white">
               <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" />
            </div>
          </div>
        </nav>
      </div>

      <div className="max-w-[1400px] mx-auto px-6 mt-10">
        <h1 className="text-5xl font-extrabold tracking-tight text-[#111] mb-8">Churn Predictor</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Dark Dashboard (Left 2 columns) */}
          <div className="lg:col-span-2 space-y-6">
            <div className="dark-card p-8 relative overflow-hidden">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-4">
                  <div className="bg-[#faff00] text-black px-4 py-2 rounded-full font-bold text-sm flex items-center gap-2">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                    Data Input
                  </div>
                  <span className="text-gray-400 font-medium">Customer Behavior & Demographics</span>
                </div>
                <div className="flex gap-2">
                  <div className="w-8 h-8 rounded border border-gray-600 flex items-center justify-center text-gray-400 hover:text-white cursor-pointer"><svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 6h16M4 12h16M4 18h16"></path></svg></div>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="relative z-10">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6 mb-8">
                  
                  {/* Form Fields */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-gray-300 text-sm font-semibold">Age</label>
                      <span className="text-[#faff00] text-sm font-bold">{formData.age} yrs</span>
                    </div>
                    <input type="range" name="age" min="18" max="80" value={formData.age} onChange={handleChange} className="yellow-slider" />
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-gray-300 text-sm font-semibold">Services Opted</label>
                      <span className="text-[#faff00] text-sm font-bold">{formData.services}</span>
                    </div>
                    <input type="range" name="services" min="1" max="6" value={formData.services} onChange={handleChange} className="yellow-slider" />
                  </div>

                  <div>
                    <label className="block text-gray-300 text-sm font-semibold mb-2">Frequent Flyer</label>
                    <select name="freqFlyer" value={formData.freqFlyer} onChange={handleChange} className="dark-input">
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-300 text-sm font-semibold mb-2">Annual Income</label>
                    <select name="income" value={formData.income} onChange={handleChange} className="dark-input">
                      <option value="Low Income">Low Income</option>
                      <option value="Middle Income">Middle Income</option>
                      <option value="High Income">High Income</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-300 text-sm font-semibold mb-2">Social Media Synced</label>
                    <select name="social" value={formData.social} onChange={handleChange} className="dark-input">
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-300 text-sm font-semibold mb-2">Hotel Booked</label>
                    <select name="hotel" value={formData.hotel} onChange={handleChange} className="dark-input">
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-end pt-4 border-t border-gray-700">
                  <button type="submit" disabled={loading} className="yellow-btn">
                    {loading ? 'Analyzing...' : 'Generate Prediction'}
                  </button>
                </div>
              </form>
              
              {/* Decorative background element */}
              <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-[#faff00] opacity-5 rounded-full blur-3xl pointer-events-none"></div>
            </div>
          </div>

          {/* Right Column Dark Panels */}
          <div className="space-y-6">
            <div className="dark-card p-6 h-[220px] flex flex-col justify-between relative overflow-hidden">
              <div className="flex justify-between items-start z-10 relative">
                <span className="text-gray-400 font-medium">Risk KPI</span>
                <div className="bg-[#1a1a1a] px-3 py-1 rounded-lg text-xs border border-gray-700 text-gray-300">
                  Real-time
                </div>
              </div>
              <div className="z-10 relative">
                <h2 className="text-6xl font-bold tracking-tighter">
                  {prediction ? `${prediction.prob.toFixed(1)}%` : '--'}
                </h2>
                <p className="text-gray-400 mt-2 text-sm">Churn Probability</p>
              </div>
              {/* Abstract chart graphic at the bottom */}
              <div className="absolute bottom-0 left-0 w-full h-24 pointer-events-none">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="w-full h-full opacity-20">
                  <path d="M0,100 L0,50 Q25,30 50,60 T100,20 L100,100 Z" fill="#faff00" />
                </svg>
              </div>
            </div>

            <div className="dark-card p-6 h-[180px]">
              <span className="text-gray-400 font-medium mb-4 block">Status Indicators</span>
              <div className="flex gap-4">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 ${prediction && prediction.pred === 1 ? 'border-[#ff4b4b] bg-[#ff4b4b] bg-opacity-20' : 'border-gray-700 bg-[#1a1a1a]'}`}>
                  <div className={`w-4 h-4 rounded-full ${prediction && prediction.pred === 1 ? 'bg-[#ff4b4b] shadow-[0_0_10px_#ff4b4b]' : 'bg-gray-600'}`}></div>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 ${prediction && prediction.prob > 40 && prediction.pred !== 1 ? 'border-[#ffa94d] bg-[#ffa94d] bg-opacity-20' : 'border-gray-700 bg-[#1a1a1a]'}`}>
                  <div className={`w-4 h-4 rounded-full ${prediction && prediction.prob > 40 && prediction.pred !== 1 ? 'bg-[#ffa94d] shadow-[0_0_10px_#ffa94d]' : 'bg-gray-600'}`}></div>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 ${prediction && prediction.prob <= 40 ? 'border-[#51cf66] bg-[#51cf66] bg-opacity-20' : 'border-gray-700 bg-[#1a1a1a]'}`}>
                  <div className={`w-4 h-4 rounded-full ${prediction && prediction.prob <= 40 ? 'bg-[#51cf66] shadow-[0_0_10px_#51cf66]' : 'bg-gray-600'}`}></div>
                </div>
              </div>
              <p className="text-gray-500 text-xs mt-4">Red: Critical / Yellow: Warning / Green: Safe</p>
            </div>
          </div>
        </div>

        {/* Lower Light Section */}
        {prediction && (
          <div className="mt-8 bg-gradient-to-b from-[#e1e2e4] to-[#f5f6f8] rounded-[2rem] p-8 shadow-[0_10px_40px_-10px_rgba(0,0,0,0.1)] border border-white">
            <div className="flex items-center justify-between border-b border-gray-300 pb-4 mb-8">
              <div className="flex items-center gap-3">
                <svg width="20" height="20" fill="none" stroke="#666" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                <h3 className="text-xl font-bold text-gray-800">Prediction Statement Report <span className="text-gray-400 font-normal">/ AI Insight</span></h3>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-sm font-medium text-gray-500 flex items-center gap-2"><svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg> Today</div>
                <button className="yellow-btn !py-2 !px-6 !text-sm">Export Report</button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Detailed statement */}
              <div className="light-card p-8">
                <div className="flex justify-between items-center mb-6">
                  <h4 className="text-lg font-bold text-gray-800">Confidence Statement</h4>
                  <div className="flex gap-2 text-gray-400">
                    <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path><path d="M12 8v4"></path><path d="M12 16h.01"></path></svg>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-6 mb-8">
                  <div>
                    <p className="text-sm text-gray-500 font-medium mb-1">Retention Probability</p>
                    <p className="text-2xl font-extrabold text-gray-800">{(100 - prediction.prob).toFixed(2)}%</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 font-medium mb-1">Churn Probability</p>
                    <p className="text-2xl font-extrabold text-gray-800">{prediction.prob.toFixed(2)}%</p>
                  </div>
                </div>

                {/* Progress bars matching the image style */}
                <div className="flex h-3 rounded-full overflow-hidden mb-8 bg-gray-200">
                  <div className="bg-[#1a1a1a]" style={{ width: `${100 - prediction.prob}%` }}></div>
                  <div className="bg-[#e0e0e0] w-2"></div>
                  <div className="bg-[#faff00]" style={{ width: `${prediction.prob}%` }}></div>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center border-b border-gray-100 pb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-4 h-4 rounded-full bg-[#1a1a1a]"></div>
                      <span className="text-gray-600 font-medium">Will Not Churn</span>
                    </div>
                    <span className="font-bold">{(100 - prediction.prob).toFixed(2)}%</span>
                  </div>
                  <div className="flex justify-between items-center pb-2">
                    <div className="flex items-center gap-3">
                      <div className="w-4 h-4 rounded-full bg-[#faff00]"></div>
                      <span className="text-gray-600 font-medium">Will Churn</span>
                    </div>
                    <span className="font-bold">{prediction.prob.toFixed(2)}%</span>
                  </div>
                </div>
              </div>

              {/* Action summary */}
              <div className="space-y-6">
                <div className="light-card p-8 h-full">
                  <div className="flex items-center gap-3 mb-6">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                    <h4 className="text-lg font-bold text-gray-800">Assistant Summary</h4>
                  </div>
                  
                  {prediction.pred === 1 ? (
                    <div className="mb-6">
                      <p className="text-gray-600 font-medium leading-relaxed">
                        The model predicts that this client will <strong className="text-black">abandon the service</strong> with a confidence of <strong className="text-black">{prediction.prob.toFixed(1)}%</strong>. 
                      </p>
                      <p className="text-gray-600 font-medium mt-4">
                        <strong className="text-[#ff4b4b]">Action Required:</strong> Immediate retention campaign necessary.
                      </p>
                    </div>
                  ) : prediction.prob > 40 ? (
                    <div className="mb-6">
                      <p className="text-gray-600 font-medium leading-relaxed">
                        The model indicates an <strong className="text-black">elevated risk</strong> of churn at <strong className="text-black">{prediction.prob.toFixed(1)}%</strong>.
                      </p>
                      <p className="text-gray-600 font-medium mt-4">
                        <strong className="text-[#ffa94d]">Recommendation:</strong> Proactive engagement and special incentives.
                      </p>
                    </div>
                  ) : (
                    <div className="mb-6">
                      <p className="text-gray-600 font-medium leading-relaxed">
                        The model suggests the client is <strong className="text-black">stable</strong> with only a <strong className="text-black">{prediction.prob.toFixed(1)}%</strong> risk of leaving.
                      </p>
                      <p className="text-gray-600 font-medium mt-4">
                        <strong className="text-[#51cf66]">Recommendation:</strong> Continue normal service delivery and explore upsell opportunities.
                      </p>
                    </div>
                  )}

                  {/* Visual blocks matching the image's layout on the right side */}
                  <div className="mt-auto flex items-end justify-between pt-8 border-t border-gray-100">
                     <div className="flex flex-col gap-2">
                       <span className="text-xs text-gray-400 font-semibold uppercase">Risk Level</span>
                       <div className="flex items-end gap-2 h-16">
                         <div className="w-16 bg-gray-200 h-10 rounded"></div>
                         <div className="w-16 bg-[#1a1a1a] h-12 rounded"></div>
                         <div className="w-20 bg-[#faff00] h-6 rounded flex items-center justify-center text-[10px] font-bold">
                            {prediction.pred === 1 ? 'HIGH' : prediction.prob > 40 ? 'MED' : 'LOW'}
                         </div>
                       </div>
                     </div>
                     <span className="text-lg font-black">{prediction.prob.toFixed(1)}%<span className="text-xs text-[#ff4b4b] ml-1">↑</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
