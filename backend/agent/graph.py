from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict):
    raw_csv_path: str
    anomalies: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]] 
    remediation_code: str
    executive_report: str
    human_feedback: str