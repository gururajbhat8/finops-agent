import json
import boto3
import os
from backend.agent.graph import app as finops_workflow

# Initialize the AWS S3 Client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda entry point. 
    Triggered automatically by S3 Event Notifications when a file is uploaded.
    """
    try:
        # 1. AWS passes 'event' data. We extract the bucket and file name from it.
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        
        print(f"🚀 Triggered by new file: {file_key} in bucket: {bucket_name}")
        
        # 2. Safety Check: Only process files in the 'input/' folder
        if not file_key.startswith("input/"):
            return {"statusCode": 200, "body": "Ignored. File is not in the input folder."}
            
        # 3. Lambda has a read-only file system, EXCEPT for the /tmp/ directory.
        # We must download the CSV from S3 to /tmp/ so Pandas can read it.
        local_temp_path = f"/tmp/{os.path.basename(file_key)}"
        s3_client.download_file(bucket_name, file_key, local_temp_path)
        
        # 4. Run the AI Workflow (The exact same code we ran locally!)
        print("Starting FinOps AI Workflow...")
        initial_state = {"raw_csv_path": local_temp_path}
        final_state = finops_workflow.invoke(initial_state)
        
        # 5. Format the AI's output
        output_data = {
            "executive_report": final_state["executive_report"],
            "remediation_code": final_state["remediation_code"]
        }
        
        # 6. Change the file path from input/ to output/, and save it as a JSON file
        output_key = file_key.replace("input/", "output/").replace(".csv", "_results.json")
        
        # 7. Upload the final results back to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(output_data, indent=2)
        )
        
        print(f"✅ Success! Results saved to s3://{bucket_name}/{output_key}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "FinOps Audit Complete", "output_file": output_key})
        }
        
    except Exception as e:
        print(f"❌ Error processing S3 event: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
