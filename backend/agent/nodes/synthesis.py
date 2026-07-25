from backend.core.config import get_llm


def synthesis_node(state: dict) -> dict: 
    """
    Acts as an Executive Cloud Consultant.
    Drafts a professional business report summarizing the FinOps findings for leadership.
    """
    print("\n👔 Synthesis Agent is drafting the executive report...")

    anomalies = state.get("anomalies", [])

    recommendations = state.get("recommendations", [])

    if not anomalies:
        return {
            "executive_report": "All clear. No cost anomalies found in the infrastructure."
        }

    llm = get_llm()

    prompt = f"""
    You are an Executive Cloud Consultant summarizing a FinOps audit.
    
    Here are the raw anomalies found:
    {anomalies}
    
    Here are the technical recommendations we are executing:
    {recommendations}
    
    Draft a highly professional, client-facing executive report. 
    Use clean markdown formatting. 
    Must include:
    1. Executive Summary (High-level overview of wasted spend).
    2. Key Findings (Breakdown of the major issues).
    3. Recommended Actions.
    4. Business Value (Explain the ROI of fixing this).
    
    Maintain a polished, corporate tone suitable for C-level executives (CTO/CFO).
    """

    print("  -> Generating business report...")

    response = llm.invoke(prompt)

    return {"executive_report": response.content}