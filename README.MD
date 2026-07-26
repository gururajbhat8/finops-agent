# 🤖 Enterprise Autonomous FinOps Agent

An event-driven, multi-agent AI architecture designed to autonomously audit AWS cloud infrastructure, identify wasted spend, and generate executable remediation code with Human-In-The-Loop (HITL) safety mechanisms.

## 🏗️ Architecture & Tech Stack
**Core Technologies:** Python, LangGraph, LangChain, Pandas, Docker, Streamlit
**AWS Services:**
- **Amazon Bedrock:** Hosting the Amazon Nova Pro foundation model.
- **Amazon S3:** Triggering automated pipelines via Event Notifications.
- **AWS Lambda:** Serverless execution of the AI workflow.
- **Amazon EKS (Kubernetes):** High-availability hosting for the Streamlit dashboard.
- **AWS Secrets Manager:** Secure credential injection.

## 🚀 Version Roadmap
- **[v1.0] Current Architecture:** 
  - Pandas Data Pipeline for metric thresholding.
  - 4-Agent LangGraph Workflow (Analyst, Architect, DevOps, Synthesis).
  - Streamlit Human-in-the-Loop Dashboard (Dockerized).
  - S3 -> Lambda Event-Driven Automation.
- **[v2.0] Incoming (Microservices):** 
  - **FastAPI Integration:** Decoupling the Streamlit frontend from the LangGraph backend by introducing a FastAPI REST layer to allow multi-platform triggers (e.g., Slack bots, Cron jobs).

## 🧠 Multi-Agent Workflow
1. **Data Analyst (Pandas):** Filters raw AWS Cost & Usage Reports for orphaned or underutilized resources.
2. **Solutions Architect (Nova Pro):** Evaluates anomalies and decides on architectural fixes.
3. **DevOps Engineer (Nova Pro):** Writes raw, executable `boto3` Python scripts to implement the fixes.
4. **Synthesis Agent (Nova Pro):** Drafts a C-level executive markdown report calculating ROI.

## 💻 Local Setup
1. Clone the repository and install dependencies: `pip install -r requirements.txt`
2. Add your AWS keys to a `.env` file.
3. Run the dashboard: `streamlit run app.py`
