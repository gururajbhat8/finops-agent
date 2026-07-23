import os 
from dotenv import load_dotenv 
from langchain_aws import ChatBedrock

load_dotenv() 

def get_llm():
    """
    We are using Claude 3 Haiku because it is incredibly fast and cheap, 
    but still smart enough to write AWS code.
    """

    print("🤖 Waking up Claude 3 via AWS Bedrock...")

    llm = ChatBedrock(
        model_id="amazon.nova-pro-v1:0",
        model_kwargs={"temperature": 0.0} 
    )

    return llm


# Quick test to make sure AWS credentials are working!
if __name__ == "__main__":
    test_llm = get_llm()
    response = test_llm.invoke("Hello, are you connected to AWS Bedrock?")
    print(response.content)