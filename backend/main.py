import os 
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil

from backend.agent.graph import app as finops_workflow


api = FastAPI(title="FinOps Agent API", version="2.0")

@api.post("/api/audit")
async def audit_cloud_costs(file: UploadFile = File(...)):
    """
    Accepts a CSV file via REST API, runs the LangGraph AI workflow, 
    and returns the optimized FinOps report.
    """
    pass