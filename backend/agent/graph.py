from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

from backend.agent.nodes.data_analyst import analyze_billing_data
from backend.agent.nodes.architect import architect_node
from backend.agent.nodes.devops import devops_node
from backend.agent.nodes.synthesis import synthesis_node


class GraphState(TypedDict):
    raw_csv_path: str
    anomalies: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]] 
    remediation_code: str
    executive_report: str
    human_feedback: str


def data_analyst_node(state: dict) -> dict: 
    csv_path = state.get("raw_csv_path", "data/mock_billing_data.csv")

    found_anomalies = analyze_billing_data(csv_path)

    return {"anomalies": found_anomalies}

workflow = StateGraph(GraphState)

workflow.add_node("DataAnalyst", data_analyst_node)
workflow.add_node("Architect", architect_node)
workflow.add_node("DevOps", devops_node)
workflow.add_node("Synthesis", synthesis_node)


workflow.add_edge(START, "DataAnalyst")
workflow.add_edge("DataAnalyst", "Architect")
workflow.add_edge("Architect", "DevOps")
workflow.add_edge("DevOps", "Synthesis")
workflow.add_edge("Synthesis", END)

app = workflow.compile()


# --- TEST THE GRAPH ---
if __name__ == "__main__":
    print("🚀 Starting the Autonomous FinOps Agent...\n")

    initial_state = {"raw_csv_path": "data/mock_billing_data.csv"}
    
    # Run the graph!
    final_state = app.invoke(initial_state)
    
    print("\n✅ WORKFLOW COMPLETE!")
    print("\n--- GENERATED CODE ---")
    print(final_state["remediation_code"])
    print("\n--- EXECUTIVE REPORT ---")
    print(final_state["executive_report"])