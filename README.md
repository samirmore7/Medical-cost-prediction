# Medical-cost-prediction
https://medical-cost-prediction-novj.onrender.com/

# 💻 Laptop Purchase Prediction System

An end-to-end Machine Learning web application and analytics dashboard that predicts customer laptop purchase decisions based on demographic and financial parameters. Built using Python, Flask, and Scikit-Learn, and styled with modern glassmorphism UI, real-time Chart.js visualizations, and dynamic theme switching.

---

## 🌟 Key Features

- **Real-Time ML Inferences**: Instant classification (`YES` / `NO`) powered by a pre-trained `DecisionTreeClassifier` (`DTML.pkl`).
- **Interactive Analytics Dashboard**:
  - **Probability Distribution**: Live Chart.js doughnut chart showing confidence breakdown.
  - **Feature Benchmark Comparison**: Bar chart comparing customer parameters against standardized indices.
  - **Session History Log**: Real-time table logging past predictions dynamically without page reloads.
- **Multiple Premium Themes**: Toggle between 5 custom visual themes (Dark, Light, Cyberpunk, Emerald, and Luxury Gold).
- **Production Ready**: Fully configured for serverless deployment on **Vercel** or cloud hosting on **AWS (EC2 / App Runner)**.

---

## 🛠️ Tech Stack & Dependencies

- **Backend**: Python 3.11+, Flask 3.0.2, Gunicorn
- **Machine Learning**: Scikit-Learn 1.6.1, NumPy 2.2.3, Pickle
- **Frontend**: HTML5, CSS3 (Glassmorphism & CSS Variables), JavaScript (Fetch API)
- **Data Visualization**: Chart.js, FontAwesome 6, Google Fonts (Plus Jakarta Sans, Space Grotesk)

---

## 📂 Project Directory Structure

```text
Laptop-Purchase-Prediction/
├── app.py              # Core Flask application and single-page dashboard UI
├── DTML.pkl            # Pre-trained Scikit-Learn Decision Tree model
├── requirements.txt    # Dependencies and version locks
├── Procfile            # Deployment configuration for Gunicorn
├── vercel.json         # Deployment configuration for Vercel Serverless
├── Dockerfile          # Container configuration for AWS / Docker
└── README.md           # Project documentation
🚀 Decision Logic Overview
The model evaluates inputs using key thresholds:

Age > 30 & Income > $50,000: Predicts YES (High purchase likelihood)

Age > 30 & Income ≤ $50,000: Predicts NO

Age ≤ 30 & Occupation in (Professional, Self-Employed): Predicts YES

Age ≤ 30 & Occupation in (Student, Unemployed, Retired): Predicts NO

💻 Local Setup & Installation
1. Clone the Repository
Bash
git clone [https://github.com/your-username/laptop-purchase-prediction.git](https://github.com/your-username/laptop-purchase-prediction.git)
cd laptop-purchase-prediction
2. Create and Activate Virtual Environment
Bash
python3 -m venv venv
source venv/bin/activate        # On Linux/macOS
# venv\Scripts\activate          # On Windows
3. Install Requirements
Bash
pip install -r requirements.txt
4. Run the Flask App
Bash
python3 app.py
Open http://127.0.0.1:8080 in your browser.

☁️ Deployment Instructions
Option 1: Deploy on AWS EC2
SSH into your EC2 instance.

Clone your repository and install dependencies inside venv:

Bash
pip install -r requirements.txt
Run the application with Gunicorn on port 8080:

Bash
gunicorn --bind 0.0.0.0:8080 app:app
Ensure your AWS Security Group Inbound Rules permit Custom TCP traffic on port 8080.

Access via http://<YOUR-EC2-PUBLIC-IP>:8080.

Option 2: Deploy on Vercel
Import your GitHub repository into Vercel.

Vercel automatically detects vercel.json and routes traffic to app.py.

Click Deploy.

Option 3: Deploy with Docker / AWS App Runner
Build the Docker image:

Bash
docker build -t laptop-purchase-app .
Run locally:

Bash
docker run -p 8080:8080 laptop-purchase-app
Connect repository directly to AWS App Runner or AWS Elastic Beanstalk using the provided Dockerfile.
