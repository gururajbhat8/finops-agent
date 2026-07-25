from backend.core.config import get_llm

def architect_node(state: dict) -> dict: 
    """
    Acts as an AWS Solutions Architect.
    Takes the anomalies found by the Data Analyst and decides how to fix them.
    """
    print("\n🧠 Architect Agent is analyzing the anomalies...")

    anomalies = state.get("anomalies", []) 
    recommendations = [] 

    llm = get_llm()

    for anomaly in anomalies:
        print(f"  -> Consulting AI for {anomaly['resource_id']}...")

        prompt = f"""
        You are a strict AWS Solutions Architect expert in FinOps and Cost Optimization.
        A Data Analyst has flagged the following AWS resource for wasting money:

        Resource ID: {anomaly['resource_id']}
        Issue: {anomaly['issue']}
        Details: {anomaly['details']}
        Raw Data: {anomaly['raw_data']}
        
        Provide a concise, 1-2 sentence recommendation on how to remediate this issue 
        using AWS best practices. Do NOT write any Python or Boto3 code. Just state the architectural fix.
        """

        
        response = llm.invoke(prompt)

        recommendations.append({
            "resource_id": anomaly['resource_id'], 
            "issue": anomaly['issue'], 
            "recommendation": response.content
        })


    return {"recommendations": recommendations}
