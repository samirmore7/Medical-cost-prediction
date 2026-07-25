import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Load pickle model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'Model.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Mapping values for human-readable inputs
SEX_MAP = {'male': 1, 'female': 0}
SMOKER_MAP = {'yes': 1, 'no': 0}
REGION_MAP = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="netflix">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Guard - Premium Insurance Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;700;900&family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root[data-theme="netflix"] {
            --bg-primary: #141414;
            --bg-secondary: #181818;
            --bg-card: rgba(32, 32, 32, 0.75);
            --accent: #E50914;
            --accent-hover: #F40612;
            --text-main: #FFFFFF;
            --text-sub: #AAAAAA;
            --border-color: rgba(255, 255, 255, 0.12);
            --glow-color: rgba(229, 9, 20, 0.4);
            --glass-border: rgba(229, 9, 20, 0.25);
        }

        :root[data-theme="cyberpunk"] {
            --bg-primary: #03071e;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.8);
            --accent: #06b6d4;
            --accent-hover: #22d3ee;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --border-color: rgba(6, 182, 212, 0.2);
            --glow-color: rgba(6, 182, 212, 0.5);
            --glass-border: rgba(6, 182, 212, 0.3);
        }

        :root[data-theme="gold"] {
            --bg-primary: #0b0c10;
            --bg-secondary: #1f2833;
            --bg-card: rgba(31, 40, 51, 0.8);
            --accent: #d4af37;
            --accent-hover: #f39c12;
            --text-main: #ffffff;
            --text-sub: #c5a059;
            --border-color: rgba(212, 175, 55, 0.2);
            --glow-color: rgba(212, 175, 55, 0.4);
            --glass-border: rgba(212, 175, 55, 0.3);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Helvetica Neue', 'Poppins', sans-serif;
            transition: background-color 0.4s ease, color 0.3s ease, border-color 0.3s ease;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, var(--glow-color) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0,0,0,0.8) 0%, transparent 50%);
        }

        /* Netflix Header Style */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 50px;
            background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, transparent 100%);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }

        .logo {
            font-size: 2rem;
            font-weight: 900;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 15px var(--glow-color);
        }

        .theme-selector {
            display: flex;
            gap: 10px;
            background: rgba(0, 0, 0, 0.5);
            padding: 6px;
            border-radius: 30px;
            border: 1px solid var(--border-color);
        }

        .theme-btn {
            background: transparent;
            border: none;
            color: var(--text-sub);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .theme-btn.active {
            background: var(--accent);
            color: #fff;
            box-shadow: 0 0 12px var(--glow-color);
        }

        /* Layout Container */
        .main-container {
            max-width: 1300px;
            margin: 30px auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
        }

        @media (max-width: 968px) {
            .main-container {
                grid-template-columns: 1fr;
            }
        }

        /* Premium Glass Card */
        .card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 35px;
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.8s ease-out;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: 0.5s;
        }

        .card:hover::before {
            left: 100%;
        }

        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--text-main);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 12px;
        }

        .card-title i {
            color: var(--accent);
        }

        /* Input Form Elements */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .input-group.full-width {
            grid-column: span 2;
        }

        label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-sub);
            font-weight: 600;
        }

        input, select {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            padding: 14px 16px;
            border-radius: 8px;
            color: var(--text-main);
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 10px var(--glow-color);
            background: rgba(0, 0, 0, 0.6);
        }

        select option {
            background: var(--bg-secondary);
            color: var(--text-main);
        }

        /* Netflix Premium Button Animation */
        .btn-premium {
            width: 100%;
            margin-top: 30px;
            padding: 16px;
            background: var(--accent);
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 6px 20px var(--glow-color);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        .btn-premium:hover {
            background: var(--accent-hover);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 25px var(--glow-color);
        }

        .btn-premium:active {
            transform: translateY(1px) scale(0.98);
        }

        /* Dashboard Results & Recommendation Section */
        .result-box {
            text-align: center;
            padding: 30px 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border: 1px dashed var(--border-color);
            margin-bottom: 25px;
        }

        .result-box .amount {
            font-size: 3rem;
            font-weight: 900;
            color: var(--accent);
            margin: 10px 0;
            text-shadow: 0 0 20px var(--glow-color);
        }

        .recommendations-wrapper {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .rec-card {
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid var(--accent);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            display: flex;
            align-items: flex-start;
            gap: 15px;
            transition: transform 0.3s ease;
            cursor: pointer;
        }

        .rec-card:hover {
            transform: translateX(8px);
            background: rgba(255, 255, 255, 0.07);
        }

        .rec-card i {
            font-size: 1.5rem;
            color: var(--accent);
            margin-top: 2px;
        }

        .rec-title {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 4px;
        }

        .rec-desc {
            font-size: 0.85rem;
            color: var(--text-sub);
            line-height: 1.4;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .pulse {
            animation: pulse-animation 2s infinite;
        }

        @keyframes pulse-animation {
            0% { box-shadow: 0 0 0 0 var(--glow-color); }
            70% { box-shadow: 0 0 0 15px rgba(0, 0, 0, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
        }
    </style>
</head>
<body>

    <nav class="navbar">
        <div class="logo">
            <i class="fa-solid fa-shield-halved"></i> HealthGuard
        </div>
        <div class="theme-selector">
            <button class="theme-btn active" onclick="setTheme('netflix')">Netflix</button>
            <button class="theme-btn" onclick="setTheme('cyberpunk')">Cyberpunk</button>
            <button class="theme-btn" onclick="setTheme('gold')">Gold Luxury</button>
        </div>
    </nav>

    <div class="main-container">
        <!-- Input Form Side -->
        <div class="card">
            <div class="card-title">
                <i class="fa-solid fa-sliders"></i> Premium Policy Predictor
            </div>

            <form id="predictionForm" onsubmit="calculateInsurance(event)">
                <div class="form-grid">
                    <div class="input-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" required min="18" max="100" value="28" placeholder="e.g. 28">
                    </div>

                    <div class="input-group">
                        <label for="sex">Gender</label>
                        <select id="sex" required>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label for="bmi">BMI Index</label>
                        <input type="number" step="0.1" id="bmi" required min="10" max="60" value="24.5" placeholder="e.g. 24.5">
                    </div>

                    <div class="input-group">
                        <label for="children">Children</label>
                        <input type="number" id="children" required min="0" max="10" value="0">
                    </div>

                    <div class="input-group">
                        <label for="smoker">Smoker Status</label>
                        <select id="smoker" required>
                            <option value="no">Non-Smoker</option>
                            <option value="yes">Smoker</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label for="region">Region</label>
                        <select id="region" required>
                            <option value="southwest">Southwest</option>
                            <option value="southeast">Southeast</option>
                            <option value="northwest">Northwest</option>
                            <option value="northeast">Northeast</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="btn-premium pulse" id="submitBtn">
                    <i class="fa-solid fa-bolt"></i> Generate Premium Quote
                </button>
            </form>
        </div>

        <!-- Dashboard Analysis Side -->
        <div class="card">
            <div class="card-title">
                <i class="fa-solid fa-chart-pie"></i> Premium Analytics & Insights
            </div>

            <div class="result-box">
                <span style="color: var(--text-sub); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">Estimated Annual Premium</span>
                <div class="amount" id="predictedCost">$0.00</div>
                <span id="riskBadge" style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">
                    Awaiting Input
                </span>
            </div>

            <div class="card-title" style="font-size: 1.1rem; margin-bottom: 15px;">
                <i class="fa-solid fa-star"></i> Recommended Coverage & Plans
            </div>

            <div class="recommendations-wrapper" id="recommendationsList">
                <div class="rec-card">
                    <i class="fa-solid fa-circle-info"></i>
                    <div>
                        <div class="rec-title">Smart Recommendation Engine</div>
                        <div class="rec-desc">Fill out your profile details on the left and submit to view personalized plan recommendations.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function setTheme(themeName) {
            document.documentElement.setAttribute('data-theme', themeName);
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.innerText.toLowerCase().includes(themeName.toLowerCase())) {
                    btn.classList.add('active');
                }
            });
        }

        async function calculateInsurance(e) {
            e.preventDefault();

            const submitBtn = document.getElementById('submitBtn');
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

            const payload = {
                age: parseFloat(document.getElementById('age').value),
                sex: document.getElementById('sex').value,
                bmi: parseFloat(document.getElementById('bmi').value),
                children: parseInt(document.getElementById('children').value),
                smoker: document.getElementById('smoker').value,
                region: document.getElementById('region').value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Update Cost Display
                    document.getElementById('predictedCost').innerText = '$' + data.prediction.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                    
                    // Risk Badge
                    const riskBadge = document.getElementById('riskBadge');
                    riskBadge.innerText = data.risk_category + ' Risk Rating';
                    riskBadge.style.color = data.risk_color;
                    riskBadge.style.borderColor = data.risk_color;

                    // Update Recommendations
                    const recContainer = document.getElementById('recommendationsList');
                    recContainer.innerHTML = '';

                    data.recommendations.forEach(item => {
                        recContainer.innerHTML += `
                            <div class="rec-card" onclick="alert('Accessing ${item.title} details...')">
                                <i class="${item.icon}"></i>
                                <div>
                                    <div class="rec-title">${item.title}</div>
                                    <div class="rec-desc">${item.desc}</div>
                                </div>
                            </div>
                        `;
                    });
                } else {
                    alert('Error making prediction: ' + data.message);
                }
            } catch (err) {
                alert('Connection error occurred.');
            } finally {
                submitBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> Generate Premium Quote';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'status': 'error', 'message': 'Model file not found or corrupted.'}), 500

    try:
        data = request.get_json()

        # Map categorical variables properly
        age = float(data.get('age', 0))
        sex = SEX_MAP.get(data.get('sex', '').lower(), 0)
        bmi = float(data.get('bmi', 0.0))
        children = int(data.get('children', 0))
        smoker = SMOKER_MAP.get(data.get('smoker', '').lower(), 0)
        region = REGION_MAP.get(data.get('region', '').lower(), 0)

        # Features order matching model expected signature: ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        features = np.array([[age, sex, bmi, children, smoker, region]])
        prediction = float(model.predict(features)[0])

        # Dynamic risk categorizations & tailored recommendations
        recommendations = []
        if smoker == 1:
            risk_category = "High"
            risk_color = "#E50914"
            recommendations.append({
                'title': 'Critical Care & Smoking Cessation Rider',
                'desc': 'Includes specialized pulmonary checkups and smoking cessation support programs.',
                'icon': 'fa-solid fa-heart-pulse'
            })
        elif bmi > 30:
            risk_category = "Moderate"
            risk_color = "#f39c12"
            recommendations.append({
                'title': 'Wellness & Metabolic Health Cover',
                'desc': 'Provides discounts on health tracking, gym memberships, and nutritionist counseling.',
                'icon': 'fa-solid fa-weight-scale'
            })
        else:
            risk_category = "Low"
            risk_color = "#2ecc71"
            recommendations.append({
                'title': 'Preferred Elite Health Plan',
                'desc': 'Standard comprehensive health coverage with 0 deductible on preventive care.',
                'icon': 'fa-solid fa-shield-cat'
            })

        if children > 0:
            recommendations.append({
                'title': 'Comprehensive Family Floater Plan',
                'desc': 'Covers pediatric visits, vaccination drives, and orthodontics for children.',
                'icon': 'fa-solid fa-people-roof'
            })

        recommendations.append({
            'title': 'Global Emergency Cashless Cover',
            'desc': 'Access to over 10,000 premium network hospitals worldwide.',
            'icon': 'fa-solid fa-globe'
        })

        return jsonify({
            'status': 'success',
            'prediction': round(prediction, 2),
            'risk_category': risk_category,
            'risk_color': risk_color,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
