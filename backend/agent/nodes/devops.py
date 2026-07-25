from backend.core.config import get_llm 

def devops_node(state: dict) -> dict:
    """
    Acts as a DevOps/Cloud Automation Engineer.
    Takes the architectural recommendations and writes the Python Boto3 code to execute them.
    """
    print("\n⚙️ DevOps Agent is writing the remediation script...")

    recommendations = state.get("recommendations", [])

    if not recommendations:
        return {
            "remediation_code" : "# No anomalies found. No code generated."
        }

    llm = get_llm() 

    prompt = f""" 
    You are an expert Senior DevOps Engineer. 
    Your Solutions Architect has provided the following recommendations to fix cloud cost anomalies:

    {recommendations}

    Write a complete, executable Python script using the 'boto3' library to implement ALL of these fixes.
    
    REQUIREMENTS:
    1. Include all necessary imports (e.g., import boto3).
    2. Group the fixes into clean, logical functions (e.g., modify_ec2_instances(), delete_ebs_volumes()).
    3. Use the exact Resource IDs provided in the recommendations.
    4. ONLY return the raw python code. Do NOT wrap it in ```python markdown blocks. Do not say "Here is your code".
    """

    print("  -> Generating Boto3 code...")

    response = llm.invoke(prompt)

    code = response.content

    if code.startwith("```python"):
        code = code.replace("```python", "").replace("```", "").strip()


    return {"remediation_code": code}