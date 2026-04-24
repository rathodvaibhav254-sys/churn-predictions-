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
    <div className="min-h-screen flex flex-col">
      <header className="header-gradient py-6 border-b border-[#00ffff22] shadow-[0_0_20px_#00ffff11]">
        <h1 className="text-center text-4xl neon-text-magenta font-black tracking-widest">
          ⚡ CHURN ORACLE ⚡
        </h1>
        <p className="text-center text-[#00ffff] font-rajdhani mt-2 tracking-[0.2em] opacity-80">
          NEURAL ENGINE v2.0
        </p>
      </header>

      <main className="flex-1 container mx-auto px-4 py-12 flex flex-col md:flex-row gap-8">
        {/* Form Section */}
        <section className="flex-1 neon-card p-8">
          <h2 className="text-2xl text-[#00ffff] border-b border-[#00ffff22] pb-3 mb-6 flex items-center gap-2">
            📋 Customer Details
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Age: {formData.age}</label>
              <input type="range" name="age" min="18" max="80" value={formData.age} onChange={handleChange} className="w-full accent-[#ff00ff]" />
            </div>

            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Frequent Flyer</label>
              <select name="freqFlyer" value={formData.freqFlyer} onChange={handleChange} className="w-full neon-input rounded-lg p-3">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>

            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Annual Income Class</label>
              <select name="income" value={formData.income} onChange={handleChange} className="w-full neon-input rounded-lg p-3">
                <option value="Low Income">Low Income</option>
                <option value="Middle Income">Middle Income</option>
                <option value="High Income">High Income</option>
              </select>
            </div>

            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Services Opted: {formData.services}</label>
              <input type="range" name="services" min="1" max="6" value={formData.services} onChange={handleChange} className="w-full accent-[#ff00ff]" />
            </div>

            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Synced to Social Media</label>
              <select name="social" value={formData.social} onChange={handleChange} className="w-full neon-input rounded-lg p-3">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>

            <div>
              <label className="block text-[#c0c0ff] mb-2 font-medium">Booked Hotel</label>
              <select name="hotel" value={formData.hotel} onChange={handleChange} className="w-full neon-input rounded-lg p-3">
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>

            <button type="submit" disabled={loading} className="w-full neon-btn py-4 rounded-xl font-bold tracking-widest mt-8">
              {loading ? 'ANALYZING...' : 'PREDICT CHURN 🚀'}
            </button>
          </form>
        </section>

        {/* Results Section */}
        <section className="flex-1">
          <h2 className="text-2xl text-[#00ffff] border-b border-[#00ffff22] pb-3 mb-6 flex items-center gap-2">
            🎲 Prediction Results
          </h2>
          
          {!prediction ? (
            <div className="neon-card p-12 text-center h-[500px] flex items-center justify-center">
              <p className="text-[#c0c0ff] text-xl opacity-60 italic">Awaiting customer data...</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Main Result Card */}
              {prediction.pred === 1 ? (
                <div className="neon-card-danger p-8 text-center">
                  <h3 className="orbitron text-3xl neon-text-red mb-4">🚨 CUSTOMER WILL CHURN</h3>
                  <p className="orbitron text-5xl font-black neon-text-red">{prediction.prob.toFixed(1)}%</p>
                  <p className="text-[#ff006688] font-bold mt-4 tracking-wider">THREAT LEVEL: CRITICAL</p>
                </div>
              ) : prediction.prob > 40 ? (
                <div className="neon-card-warn p-8 text-center">
                  <h3 className="orbitron text-3xl neon-text-orange mb-4">⚠️ CUSTOMER AT RISK</h3>
                  <p className="orbitron text-5xl font-black neon-text-orange">{prediction.prob.toFixed(1)}%</p>
                  <p className="text-[#ffaa0088] font-bold mt-4 tracking-wider">THREAT LEVEL: ELEVATED</p>
                </div>
              ) : (
                <div className="neon-card-safe p-8 text-center">
                  <h3 className="orbitron text-3xl neon-text-green mb-4">✅ CUSTOMER SECURE</h3>
                  <p className="orbitron text-5xl font-black neon-text-green">{prediction.prob.toFixed(1)}%</p>
                  <p className="text-[#00ff6688] font-bold mt-4 tracking-wider">THREAT LEVEL: MINIMAL</p>
                </div>
              )}

              {/* Recommendation Card */}
              <div className="neon-card p-6">
                <h3 className="text-xl text-[#00ffff] mb-4 border-b border-[#00ffff22] pb-2">🎯 Recommendation</h3>
                {prediction.pred === 1 ? (
                  <ul className="list-disc list-inside text-[#ff0066] space-y-2 opacity-90">
                    <li>Initiate retention campaign immediately</li>
                    <li>Offer personalized travel packages</li>
                    <li>Provide exclusive loyalty rewards</li>
                    <li>Schedule direct customer outreach</li>
                  </ul>
                ) : prediction.prob > 40 ? (
                  <ul className="list-disc list-inside text-[#ffaa00] space-y-2 opacity-90">
                    <li>Monitor customer activity</li>
                    <li>Proactive engagement campaigns</li>
                    <li>Offer special incentives</li>
                    <li>Regular check-in calls</li>
                  </ul>
                ) : (
                  <ul className="list-disc list-inside text-[#00ff66] space-y-2 opacity-90">
                    <li>Continue excellent service</li>
                    <li>Encourage loyalty program participation</li>
                    <li>Upsell additional services</li>
                    <li>Request referrals</li>
                  </ul>
                )}
              </div>
            </div>
          )}
        </section>
      </main>

      <footer className="py-6 border-t border-[#ff00ff22] mt-auto">
        <p className="text-center orbitron text-[#ff00ff88] text-xs tracking-[0.3em]">
          ⚡ NEURAL CHURN ENGINE v2.0 ⚡<br/>
          <span className="text-[10px] text-[#00ffff44]">POWERED BY RANDOM FOREST & VERCEL</span>
        </p>
      </footer>
    </div>
  );
}
