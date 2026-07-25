import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Search explicitly for Model.pkl, fallback to Model (2).pkl if needed
MODEL_NAME = 'Model.pkl' if os.path.exists('Model.pkl') else 'Model (2).pkl'
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_NAME)

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print(f"Loaded pickle model successfully from '{MODEL_NAME}'!")
except Exception as e:
    model = None
    print(f"Error loading model pickle file ({MODEL_NAME}): {e}")

# Human-readable form inputs mapped to trained feature encodings
SEX_MAP = {'male': 1, 'female': 0}
SMOKER_MAP = {'yes': 1, 'no': 0}
REGION_MAP = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="netflix">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InsurAI - Enterprise Risk & Analytics Dashboard</title>
    <!-- Google Fonts, FontAwesome, and Chart.js -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        /* -------------------------------------------------------------------------- */
        /* 10 PREMIUM THEME PALETTES                                                  */
        /* -------------------------------------------------------------------------- */
        
        :root[data-theme="basic-dark"] {
            --bg-base: #121212; --bg-card: rgba(30, 30, 30, 0.85); --bg-input: rgba(18, 18, 18, 0.6);
            --accent: #3b82f6; --accent-hover: #60a5fa; --accent-glow: rgba(59, 130, 246, 0.35);
            --text-primary: #ffffff; --text-secondary: #a1a1aa; --border-color: rgba(255, 255, 255, 0.12);
            --badge-bg: rgba(59, 130, 246, 0.15);
        }

        :root[data-theme="basic-light"] {
            --bg-base: #f8fafc; --bg-card: rgba(255, 255, 255, 0.85); --bg-input: #f1f5f9;
            --accent: #2563eb; --accent-hover: #1d4ed8; --accent-glow: rgba(37, 99, 235, 0.25);
            --text-primary: #0f172a; --text-secondary: #64748b; --border-color: rgba(15, 23, 42, 0.12);
            --badge-bg: rgba(37, 99, 235, 0.1);
        }

        :root[data-theme="netflix"] {
            --bg-base: #141414; --bg-card: rgba(24, 24, 24, 0.9); --bg-input: rgba(0, 0, 0, 0.6);
            --accent: #E50914; --accent-hover: #F40612; --accent-glow: rgba(229, 9, 20, 0.4);
            --text-primary: #FFFFFF; --text-secondary: #A3A3A3; --border-color: rgba(255, 255, 255, 0.12);
            --badge-bg: rgba(229, 9, 20, 0.15);
        }

        :root[data-theme="cyberpunk"] {
            --bg-base: #050814; --bg-card: rgba(13, 22, 40, 0.85); --bg-input: rgba(5, 11, 24, 0.7);
            --accent: #00f0ff; --accent-hover: #70f3ff; --accent-glow: rgba(0, 240, 255, 0.45);
            --text-primary: #F8FAFC; --text-secondary: #94A3B8; --border-color: rgba(0, 240, 255, 0.25);
            --badge-bg: rgba(0, 240, 255, 0.15);
        }

        :root[data-theme="glass"] {
            --bg-base: #0f172a; --bg-card: rgba(30, 41, 59, 0.75); --bg-input: rgba(15, 23, 42, 0.6);
            --accent: #6366f1; --accent-hover: #818cf8; --accent-glow: rgba(99, 102, 241, 0.4);
            --text-primary: #F8FAFC; --text-secondary: #CBD5E1; --border-color: rgba(255, 255, 255, 0.15);
            --badge-bg: rgba(99, 102, 241, 0.15);
        }

        :root[data-theme="gold"] {
            --bg-base: #0A0A0B; --bg-card: rgba(20, 20, 22, 0.9); --bg-input: rgba(10, 10, 12, 0.6);
            --accent: #D4AF37; --accent-hover: #F3C623; --accent-glow: rgba(212, 175, 55, 0.4);
            --text-primary: #FFFFFF; --text-secondary: #A1A1AA; --border-color: rgba(212, 175, 55, 0.25);
            --badge-bg: rgba(212, 175, 55, 0.12);
        }

        :root[data-theme="emerald"] {
            --bg-base: #022c22; --bg-card: rgba(6, 78, 59, 0.85); --bg-input: rgba(2, 44, 34, 0.6);
            --accent: #10b981; --accent-hover: #34d399; --accent-glow: rgba(16, 185, 129, 0.4);
            --text-primary: #ecfdf5; --text-secondary: #a7f3d0; --border-color: rgba(16, 185, 129, 0.25);
            --badge-bg: rgba(16, 185, 129, 0.15);
        }

        :root[data-theme="sunset"] {
            --bg-base: #1a0c1a; --bg-card: rgba(45, 20, 45, 0.85); --bg-input: rgba(20, 8, 20, 0.6);
            --accent: #f43f5e; --accent-hover: #fb7185; --accent-glow: rgba(244, 63, 94, 0.4);
            --text-primary: #fff1f2; --text-secondary: #fecdd3; --border-color: rgba(244, 63, 94, 0.25);
            --badge-bg: rgba(244, 63, 94, 0.15);
        }

        :root[data-theme="nordic"] {
            --bg-base: #0f172a; --bg-card: rgba(30, 41, 59, 0.85); --bg-input: rgba(15, 23, 42, 0.6);
            --accent: #38bdf8; --accent-hover: #7dd3fc; --accent-glow: rgba(56, 189, 248, 0.4);
            --text-primary: #f0f9ff; --text-secondary: #bae6fd; --border-color: rgba(56, 189, 248, 0.2);
            --badge-bg: rgba(56, 189, 248, 0.15);
        }

        :root[data-theme="amethyst"] {
            --bg-base: #130a2a; --bg-card: rgba(36, 18, 77, 0.85); --bg-input: rgba(15, 6, 36, 0.6);
            --accent: #a855f7; --accent-hover: #c084fc; --accent-glow: rgba(168, 85, 247, 0.4);
            --text-primary: #faf5ff; --text-secondary: #e9d5ff; --border-color: rgba(168, 85, 247, 0.25);
            --badge-bg: rgba(168, 85, 247, 0.15);
        }

        /* -------------------------------------------------------------------------- */
        /* GLOBAL LAYOUT & STYLES                                                    */
        /* -------------------------------------------------------------------------- */
        * {
            box-sizing: border-box;
            margin: 0; padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background-color 0.35s ease, border-color 0.35s ease, color 0.35s ease;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 15%, var(--accent-glow) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(0, 0, 0, 0.8) 0%, transparent 45%);
        }

        .navbar {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 30px; background: rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(15px); border-bottom: 1px solid var(--border-color);
            position: sticky; top: 0; z-index: 100; gap: 15px; flex-wrap: wrap;
        }

        .brand {
            display: flex; align-items: center; gap: 12px;
            font-size: 1.35rem; font-weight: 800; letter-spacing: -0.5px;
        }

        .brand i { color: var(--accent); font-size: 1.5rem; filter: drop-shadow(0 0 8px var(--accent-glow)); }

        .theme-switcher {
            display: flex; background: var(--bg-input); padding: 4px;
            border-radius: 30px; border: 1px solid var(--border-color);
            gap: 4px; overflow-x: auto; max-width: 100%;
        }

        .theme-btn {
            background: transparent; border: none; color: var(--text-secondary);
            padding: 6px 14px; border-radius: 20px; cursor: pointer;
            font-size: 0.78rem; font-weight: 600; display: flex; align-items: center;
            gap: 6px; white-space: nowrap; transition: all 0.3s ease;
        }

        .theme-btn.active { background: var(--accent); color: #FFFFFF; box-shadow: 0 0 10px var(--accent-glow); }

        .dashboard-container {
            max-width: 1400px; margin: 30px auto; padding: 0 25px;
            display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 30px; width: 100%;
        }

        @media (max-width: 1024px) { .dashboard-container { grid-template-columns: 1fr; } }

        .panel {
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 20px; padding: 30px; backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .panel-full { grid-column: 1 / -1; }

        .panel-header {
            margin-bottom: 25px; border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center;
        }

        .panel-title { font-size: 1.2rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }
        .panel-title i { color: var(--accent); }

        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
        .input-wrapper { display: flex; flex-direction: column; gap: 6px; }

        label { font-size: 0.78rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.8px; }

        input, select {
            background: var(--bg-input); border: 1px solid var(--border-color);
            border-radius: 10px; padding: 12px 14px; color: var(--text-primary);
            font-size: 0.92rem; outline: none; transition: all 0.3s ease;
        }

        input:focus, select:focus { border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        select option { background: var(--bg-base); color: var(--text-primary); }

        .btn-predict {
            grid-column: span 2; margin-top: 10px;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            color: #FFFFFF; border: none; border-radius: 12px; padding: 16px;
            font-size: 0.95rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
            cursor: pointer; position: relative; overflow: hidden; display: flex;
            justify-content: center; align-items: center; gap: 10px;
            box-shadow: 0 8px 25px var(--accent-glow); transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .btn-predict::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.6s ease;
        }

        .btn-predict:hover::before { left: 100%; }
        .btn-predict:hover { transform: translateY(-3px) scale(1.01); box-shadow: 0 12px 30px var(--accent-glow); }
        .btn-predict:active { transform: translateY(1px) scale(0.99); }

        .ripple {
            position: absolute; background: rgba(255, 255, 255, 0.5);
            border-radius: 50%; transform: scale(0); animation: ripple-effect 0.6s linear; pointer-events: none;
        }

        @keyframes ripple-effect { to { transform: scale(4); opacity: 0; } }

        .metric-card {
            background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border-color);
            border-radius: 14px; padding: 25px; text-align: center; margin-bottom: 20px;
            position: relative; overflow: hidden;
        }

        .metric-label { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--text-secondary); }
        .metric-value { font-size: 3rem; font-weight: 800; color: var(--accent); margin: 8px 0; letter-spacing: -1px; text-shadow: 0 0 18px var(--accent-glow); }

        .risk-badge {
            display: inline-flex; align-items: center; gap: 6px; background: var(--badge-bg);
            border: 1px solid var(--border-color); color: var(--text-primary); padding: 6px 14px;
            border-radius: 20px; font-size: 0.82rem; font-weight: 600;
        }

        .recommendation-list { display: flex; flex-direction: column; gap: 12px; }

        .rec-item {
            background: rgba(255, 255, 255, 0.02); border-left: 4px solid var(--accent);
            border-radius: 0 10px 10px 0; padding: 14px 16px; display: flex; gap: 14px;
            align-items: flex-start; transition: all 0.3s ease; cursor: pointer;
        }

        .rec-item:hover { background: rgba(255, 255, 255, 0.06); transform: translateX(6px); }
        .rec-item i { color: var(--accent); font-size: 1.2rem; margin-top: 2px; }

        .rec-title { font-weight: 600; font-size: 0.92rem; margin-bottom: 2px; }
        .rec-desc { font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; }

        /* ANALYTICS DASHBOARD REPORT STYLES */
        .analytics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 25px;
        }

        .stat-box {
            background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 6px;
        }

        .stat-title { font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600; }
        .stat-value { font-size: 1.4rem; font-weight: 800; color: var(--text-primary); }

        .chart-container {
            position: relative; width: 100%; height: 320px; margin-top: 15px;
        }

        @keyframes slideUp { from { opacity: 0; transform: translateY(25px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <nav class="navbar">
        <div class="brand">
            <i class="fa-solid fa-layer-group"></i> InsurAI Studio
        </div>
        
        <div class="theme-switcher">
            <button class="theme-btn active" onclick="switchTheme('netflix', this)"><i class="fa-solid fa-film"></i> Netflix</button>
            <button class="theme-btn" onclick="switchTheme('basic-light', this)"><i class="fa-solid fa-sun"></i> Basic Light</button>
            <button class="theme-btn" onclick="switchTheme('basic-dark', this)"><i class="fa-solid fa-moon"></i> Basic Dark</button>
            <button class="theme-btn" onclick="switchTheme('cyberpunk', this)"><i class="fa-solid fa-bolt"></i> Cyberpunk</button>
            <button class="theme-btn" onclick="switchTheme('glass', this)"><i class="fa-solid fa-cubes"></i> Modern</button>
            <button class="theme-btn" onclick="switchTheme('gold', this)"><i class="fa-solid fa-crown"></i> Gold</button>
            <button class="theme-btn" onclick="switchTheme('emerald', this)"><i class="fa-solid fa-gem"></i> Emerald</button>
            <button class="theme-btn" onclick="switchTheme('sunset', this)"><i class="fa-solid fa-fire"></i> Sunset</button>
            <button class="theme-btn" onclick="switchTheme('nordic', this)"><i class="fa-solid fa-snowflake"></i> Nordic</button>
            <button class="theme-btn" onclick="switchTheme('amethyst', this)"><i class="fa-solid fa-wand-magic-sparkles"></i> Amethyst</button>
        </div>
    </nav>

    <div class="dashboard-container">
        
        <!-- Risk Form Input Panel -->
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    <i class="fa-solid fa-sliders"></i> Risk Parameters
                </div>
                <span style="font-size: 0.78rem; color: var(--text-secondary);">Model: DecisionTreeRegressor</span>
            </div>

            <form id="predictionForm" onsubmit="handleFormSubmit(event)">
                <div class="form-grid">
                    
                    <div class="input-wrapper">
                        <label for="age">Age</label>
                        <input type="number" id="age" name="age" min="18" max="100" value="32" required>
                    </div>

                    <div class="input-wrapper">
                        <label for="sex">Gender Category</label>
                        <select id="sex" name="sex" required>
                            <option value="male" selected>Male</option>
                            <option value="female">Female</option>
                        </select>
                    </div>

                    <div class="input-wrapper">
                        <label for="bmi">BMI Index</label>
                        <input type="number" step="0.1" id="bmi" name="bmi" min="10" max="60" value="26.4" required>
                    </div>

                    <div class="input-wrapper">
                        <label for="children">Dependents / Children</label>
                        <input type="number" id="children" name="children" min="0" max="10" value="1" required>
                    </div>

                    <div class="input-wrapper">
                        <label for="smoker">Smoker Category</label>
                        <select id="smoker" name="smoker" required>
                            <option value="no" selected>Non-Smoker</option>
                            <option value="yes">Smoker</option>
                        </select>
                    </div>

                    <div class="input-wrapper">
                        <label for="region">Geographic Region</label>
                        <select id="region" name="region" required>
                            <option value="southwest" selected>Southwest</option>
                            <option value="southeast">Southeast</option>
                            <option value="northwest">Northwest</option>
                            <option value="northeast">Northeast</option>
                        </select>
                    </div>

                    <button type="submit" class="btn-predict" id="submitBtn">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Evaluate Risk & Predict
                    </button>

                </div>
            </form>
        </div>

        <!-- Output Quotes Panel -->
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    <i class="fa-solid fa-chart-line"></i> Live Risk Quote
                </div>
                <span style="font-size: 0.78rem; color: var(--text-secondary);">Real-Time Prediction</span>
            </div>

            <div class="metric-card">
                <div class="metric-label">Predicted Annual Premium</div>
                <div class="metric-value" id="premiumDisplay">$0.00</div>
                <div class="risk-badge" id="riskBadge">
                    <i class="fa-solid fa-shield"></i> Ready for Analysis
                </div>
            </div>

            <div class="panel-title" style="font-size: 0.95rem; margin-bottom: 12px;">
                <i class="fa-solid fa-thumbs-up"></i> Recommended Coverage Add-ons
            </div>

            <div class="recommendation-list" id="recommendationContainer">
                <div class="rec-item">
                    <i class="fa-solid fa-circle-info"></i>
                    <div>
                        <div class="rec-title">Awaiting Input Parameters</div>
                        <div class="rec-desc">Submit profile attributes to trigger automated risk rating and generate personalized coverage recommendations.</div>
                    </div>
                </div>
            </div>

        </div>

        <!-- ANALYTICS DASHBOARD REPORT PANEL -->
        <div class="panel panel-full" id="reportPanel">
            <div class="panel-header">
                <div class="panel-title">
                    <i class="fa-solid fa-microchip"></i> Analytics Dashboard Report
                </div>
                <span style="font-size: 0.78rem; color: var(--text-secondary);">Executive Summary</span>
            </div>

            <div class="analytics-grid">
                <div class="stat-box">
                    <span class="stat-title">Monthly Premium</span>
                    <span class="stat-value" id="monthlyDisplay">$0.00</span>
                </div>
                <div class="stat-box">
                    <span class="stat-title">Risk Multiplier</span>
                    <span class="stat-value" id="riskMultiplier">1.0x</span>
                </div>
                <div class="stat-box">
                    <span class="stat-title">Assigned Policy Tier</span>
                    <span class="stat-value" id="policyTier">Standard</span>
                </div>
                <div class="stat-box">
                    <span class="stat-title">Overall Health Score</span>
                    <span class="stat-value" id="healthScore">85/100</span>
                </div>
            </div>

            <div class="panel-title" style="font-size: 0.95rem; margin-top: 10px;">
                <i class="fa-solid fa-chart-bar"></i> Feature Risk Impact Breakdown
            </div>
            
            <div class="chart-container">
                <canvas id="impactChart"></canvas>
            </div>
        </div>

    </div>

    <!-- Frontend Interactive Engine -->
    <script>
        let impactChart = null;

        function switchTheme(themeName, element) {
            document.documentElement.setAttribute('data-theme', themeName);
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            element.classList.add('active');
            if (impactChart) updateChartColors();
        }

        // Animated Ripple
        document.querySelector('.btn-predict').addEventListener('click', function (e) {
            let x = e.clientX - e.target.offsetLeft;
            let y = e.clientY - e.target.offsetTop;
            let ripples = document.createElement('span');
            ripples.className = 'ripple';
            ripples.style.left = x + 'px'; ripples.style.top = y + 'px';
            this.appendChild(ripples);
            setTimeout(() => { ripples.remove(); }, 600);
        });

        // Initialize Chart.js
        function initChart() {
            const ctx = document.getElementById('impactChart').getContext('2d');
            const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();

            impactChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Age Factor', 'BMI Factor', 'Smoker Premium', 'Dependents Cost', 'Regional Rating'],
                    datasets: [{
                        label: 'Estimated Cost Contribution ($)',
                        data: [0, 0, 0, 0, 0],
                        backgroundColor: accentColor,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim() } }
                    },
                    scales: {
                        x: { ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim() }, grid: { display: false } },
                        y: { ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim() }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    }
                }
            });
        }

        function updateChartColors() {
            const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
            const textPrimary = getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim();
            const textSecondary = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim();

            impactChart.data.datasets[0].backgroundColor = accentColor;
            impactChart.options.plugins.legend.labels.color = textPrimary;
            impactChart.options.scales.x.ticks.color = textSecondary;
            impactChart.options.scales.y.ticks.color = textSecondary;
            impactChart.update();
        }

        window.onload = initChart;

        async function handleFormSubmit(event) {
            event.preventDefault();
            
            const btn = document.getElementById('submitBtn');
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

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

                const res = await response.json();

                if (res.status === 'success') {
                    // Cost & Risk
                    document.getElementById('premiumDisplay').innerText = '$' + res.prediction.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                    
                    const badge = document.getElementById('riskBadge');
                    badge.innerHTML = `<i class="fa-solid fa-shield-halved"></i> ${res.risk_category} Risk Rating`;

                    // Report Stats
                    document.getElementById('monthlyDisplay').innerText = '$' + (res.prediction / 12).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                    document.getElementById('riskMultiplier').innerText = res.risk_multiplier;
                    document.getElementById('policyTier').innerText = res.policy_tier;
                    document.getElementById('healthScore').innerText = res.health_score + '/100';

                    // Update Recommendations
                    const recContainer = document.getElementById('recommendationContainer');
                    recContainer.innerHTML = '';
                    res.recommendations.forEach(rec => {
                        recContainer.innerHTML += `
                            <div class="rec-item" onclick="alert('Accessing module: ${rec.title}')">
                                <i class="${rec.icon}"></i>
                                <div>
                                    <div class="rec-title">${rec.title}</div>
                                    <div class="rec-desc">${rec.desc}</div>
                                </div>
                            </div>
                        `;
                    });

                    // Update Chart Data
                    impactChart.data.datasets[0].data = res.feature_breakdown;
                    impactChart.update();

                } else {
                    alert('Prediction Error: ' + res.message);
                }
            } catch (err) {
                alert('Connection error occurred.');
            } finally {
                btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Evaluate Risk & Predict';
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
        return jsonify({'status': 'error', 'message': f'Model pickle file ({MODEL_NAME}) failed to load.'}), 500

    try:
        data = request.get_json()

        age = float(data.get('age', 0))
        sex = SEX_MAP.get(str(data.get('sex')).lower(), 0)
        bmi = float(data.get('bmi', 0.0))
        children = int(data.get('children', 0))
        smoker = SMOKER_MAP.get(str(data.get('smoker')).lower(), 0)
        region = REGION_MAP.get(str(data.get('region')).lower(), 0)

        features = np.array([[age, sex, bmi, children, smoker, region]])
        prediction = float(model.predict(features)[0])

        # Analytical Dashboard Metrics Calculation
        smoker_impact = 18000.0 if smoker == 1 else 0.0
        age_impact = age * 250.0
        bmi_impact = bmi * 320.0
        children_impact = children * 500.0
        region_impact = 400.0

        risk_multiplier = "1.0x"
        health_score = 100

        if smoker == 1:
            risk_category = "High"
            risk_multiplier = "2.8x"
            policyTier = "Gold Executive"
            health_score -= 35
        elif bmi > 30:
            risk_category = "Moderate"
            risk_multiplier = "1.5x"
            policyTier = "Silver Preferred"
            health_score -= 15
        else:
            risk_category = "Low"
            risk_multiplier = "1.0x"
            policyTier = "Bronze Standard"

        if bmi > 25:
            health_score -= 10
        if age > 50:
            health_score -= 10

        health_score = max(health_score, 20)

        # Dynamic Recommendations
        recommendations = []
        if smoker == 1:
            recommendations.append({
                'title': 'Pulmonary Risk & Smoking Cessation Rider',
                'desc': 'Provides routine chest screenings, specialist consultations, and free wellness coaching.',
                'icon': 'fa-solid fa-heart-pulse'
            })
        elif bmi > 30:
            recommendations.append({
                'title': 'Metabolic Health & Wellness Discount Cover',
                'desc': 'Includes gym membership reimbursements and personal nutritional counseling.',
                'icon': 'fa-solid fa-weight-scale'
            })
        else:
            recommendations.append({
                'title': 'Preferred Elite Health Cover',
                'desc': 'Zero deductible policy for preventive care and annual comprehensive checkups.',
                'icon': 'fa-solid fa-shield-cat'
            })

        if children > 0:
            recommendations.append({
                'title': 'Family Floater & Pediatric Care Add-on',
                'desc': 'Covers immunization, dental checkups, and optical care for all dependants.',
                'icon': 'fa-solid fa-people-roof'
            })

        recommendations.append({
            'title': 'Global Emergency Cashless Hospitalization',
            'desc': 'Direct cashless settlement access across 12,000+ top-tier medical facilities worldwide.',
            'icon': 'fa-solid fa-globe'
        })

        return jsonify({
            'status': 'success',
            'prediction': round(prediction, 2),
            'risk_category': risk_category,
            'risk_multiplier': risk_multiplier,
            'policy_tier': policyTier,
            'health_score': health_score,
            'feature_breakdown': [round(age_impact, 2), round(bmi_impact, 2), round(smoker_impact, 2), round(children_impact, 2), round(region_impact, 2)],
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
