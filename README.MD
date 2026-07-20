# Autonomous FinOps & Remediation Agent 🤖☁️

## Overview
This project is an enterprise-grade, multi-agent system designed to automate Cloud Financial Operations (FinOps). 
It analyzes AWS Cost & Usage Reports, identifies wasted cloud spend, cross-references anomalies with the AWS Well-Architected Framework, and autonomously generates the exact Boto3 Python scripts needed to remediate the issues.

To ensure enterprise safety, the system incorporates a **Human-In-The-Loop (HITL)** architecture. Execution pauses for a DevOps manager to review the AI-generated code and business report via a Streamlit dashboard before any changes are applied.

## Architecture & Workflow (LangGraph)
The system utilizes LangGraph for stateful, multi-agent orchestration:
1. **Data Analyst Agent:** Parses billing CSVs using Pandas to flag inefficiencies (e.g., `< 5%` CPU utilization on large EC2 instances).
2. **Solutions Architect Agent:** Evaluates flagged anomalies and determines the optimal architectural fix.
3. **DevOps Agent:** Generates executable AWS Boto3 scripts to implement the recommended fix.
4. **Executive Synthesis Agent:** Drafts a client-facing business report detailing wasted spend and projected ROI.
5. **HITL Gateway:** A Streamlit UI that halts the graph, allowing human operators to approve the generated code or provide feedback to regenerate it.

## Key Use Cases Handled
*   **EC2 Right-Sizing:** Detecting over-provisioned compute and generating scripts to modify instance types.
*   **Orphaned EBS Volumes:** Finding unattached storage volumes and generating snapshot-and-terminate scripts.
*   **S3 Lifecycle Optimization:** Identifying stale standard-tier buckets and applying Glacier transition rules.

## Tech Stack
*   **Frontend:** Streamlit
*   **Backend:** Python 3.11+, FastAPI
*   **AI/Orchestration:** LangGraph, LangChain, Amazon Bedrock / Foundation Models
*   **Data Processing:** Pandas

## Local Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/finops-agent.git
   cd finops-agent
