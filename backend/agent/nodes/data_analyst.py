import pandas as pd

def analyze_billing_data(file_path: str):
    """
    Reads the AWS billing CSV and identifies resources that are wasting money.
    Returns a list of dictionaries containing the anomalies.
    """
    print(f"🔍 Analyzing data from: {file_path}...")
    
    # 1. Load the CSV into a Pandas DataFrame
    df = pd.read_csv(file_path)
    
    anomalies = []
    
    # --- RULE 1: Underutilized EC2 Instances ---
    # Condition: It is a Compute Instance, it is currently Running, but CPU is less than 5%
    ec2_mask = (df['ResourceType'] == 'Instance') & (df['State'].str.lower() == 'running') & (df['AverageCPUUtilization'] < 5.0)
    underutilized_ec2 = df[ec2_mask]
    
    for _, row in underutilized_ec2.iterrows():
        anomalies.append({
            "resource_id": row['ResourceId'],
            "issue": "Underutilized EC2 Instance",
            "details": f"Instance {row['InstanceType_StorageClass']} is costing ${row['MonthlyCost']}/mo but only using {row['AverageCPUUtilization']}% CPU.",
            "raw_data": row.to_dict() # We keep the raw data so the LLM can see environment, team, etc.
        })
        
    # --- RULE 2: Orphaned EBS Volumes ---
    # Condition: It is a Storage Volume, but its State is 'Available' (meaning not attached to a server)
    ebs_mask = (df['ResourceType'] == 'Volume') & (df['State'].str.lower() == 'available')
    orphaned_ebs = df[ebs_mask]
    
    for _, row in orphaned_ebs.iterrows():
        anomalies.append({
            "resource_id": row['ResourceId'],
            "issue": "Orphaned EBS Volume",
            "details": f"Volume of type {row['InstanceType_StorageClass']} is costing ${row['MonthlyCost']}/mo but is not attached to any EC2 instance.",
            "raw_data": row.to_dict()
        })
        
    # --- RULE 3: Stale S3 Buckets ---
    # Condition: It is a Bucket, it's on the expensive 'Standard' tier, but hasn't been touched in over 90 days
    s3_mask = (df['ResourceType'] == 'Bucket') & (df['InstanceType_StorageClass'].str.lower() == 'standard') & (df['DaysSinceLastAccess'] > 90)
    stale_s3 = df[s3_mask]
    
    for _, row in stale_s3.iterrows():
        anomalies.append({
            "resource_id": row['ResourceId'],
            "issue": "Stale S3 Bucket",
            "details": f"Bucket is on Standard storage costing ${row['MonthlyCost']}/mo but hasn't been accessed in {row['DaysSinceLastAccess']} days.",
            "raw_data": row.to_dict()
        })

    # Print results for local testing
    print(f"⚠️ Found {len(anomalies)} anomalies in the infrastructure.")
    for a in anomalies:
        print(f"- {a['resource_id']}: {a['issue']}")
        
    return anomalies

# This block allows us to test the script directly without running the whole API
if __name__ == "__main__":
    # Point it to our CSV file. Adjust the path if you run this from a different folder!
    # Running from the root folder: `python backend/agent/nodes/data_analyst.py`
    analyze_billing_data("data/mock_billing_data.csv")
