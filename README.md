🛡️ AI Content Moderator & Analytics Dashboard
An automated safety operations system that uses Claude-3 AI and n8n to analyze and log user-generated content in real-time.

🚀 Overview
This project automates the detection of toxic content, spam, and harassment. By utilizing an n8n backend, it transforms unstructured human text into structured data for live monitoring on a Streamlit dashboard.

🛠️ Tech Stack
Automation: n8n (Workflow orchestration & Webhooks).

AI Model: Anthropic Claude-3 Haiku (via REST API).

Database: Google Sheets API.

Frontend: Python / Streamlit.

🏗️ How It Works
Ingestion: Data is sent via a POST Webhook to n8n.

AI Analysis: Claude-3 analyzes the text and returns a JSON object (Toxicity Score, Category, and Action).

Storage: n8n parses the result and appends it to a Google Sheet.

Visualization: The Streamlit dashboard displays real-time metrics and trend charts.

✨ Key Features
Real-time KPI Tracking: Live "Safety Score" and violation breakdown charts.

Human-in-the-Loop: A sidebar testing tool to manually verify AI decisions.

Scalable Architecture: Capable of handling high-volume text streams with low latency.

📦 Installation
Clone the repo and install requirements: pip install -r requirements.txt.

Add your Google Sheets credentials to .streamlit/secrets.toml.

Activate your n8n workflow and update the Webhook URL in app.py.

Run the app: streamlit run app.py.
