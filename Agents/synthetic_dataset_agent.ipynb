import os
import time
import json
import boto3
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Set up cross bedrock 
ROLE_TO_ASSUME = Path(os.path.join(os.environ["HOME"],"BedrockCrossAccount.txt")).read_text().strip()
logger.info(f"ROLE_TO_ASSUME={ROLE_TO_ASSUME}")
role_to_assume = ROLE_TO_ASSUME
import boto3
import datetime
from botocore.session import get_session
from botocore.credentials import RefreshableCredentials

# ARN of Role A to assume  
role_to_assume = ROLE_TO_ASSUME

def get_credentials():
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_to_assume,
        RoleSessionName='cross-account-session',
        # Don't set DurationSeconds when role chaining
    )
    return {
        'access_key': assumed_role['Credentials']['AccessKeyId'],
        'secret_key': assumed_role['Credentials']['SecretAccessKey'],
        'token': assumed_role['Credentials']['SessionToken'],
        'expiry_time': assumed_role['Credentials']['Expiration'].isoformat()
    }

session = get_session()
refresh_creds = RefreshableCredentials.create_from_metadata(
    metadata=get_credentials(),
    refresh_using=get_credentials,
    method='sts-assume-role'
)

# Create a new session with refreshable credentials
session._credentials = refresh_creds
boto3_session = boto3.Session(botocore_session=session)

region: str = "us-east-1"
from langchain_aws import ChatBedrockConverse
import boto3

# ---- ⚠️ Update region for your AWS setup ⚠️ ----
bedrock_client = boto3_session.client("bedrock-runtime",
                              region_name=region)

#Generate synthetic datasets
from langchain.chat_models import init_chat_model

model = init_chat_model("us.anthropic.claude-3-5-haiku-20241022-v1:0",
                        model_provider="bedrock_converse",
                        region_name="us-east-1",
                        client=bedrock_client)
from langchain_core.tools import tool
llm = ChatBedrockConverse(temperature=0, model_id="us.amazon.nova-micro-v1:0")

@tool
def generate_JSON() -> str:
    """Generate synthetic data in JSON format."""
    prompt = "Generate a synthetic dataset in a JSON array with 10 fake user records. Include name, age, and email for each record."
    response = llm.invoke(prompt)
    return response.content
    
@tool
def generate_CSV() -> str:
    """Generate synthetic data in CSV format."""
    prompt = "Generate a synthetic dataset in a CSV format with 10 fake user records. Include name, age, and email for each record."
    response = llm.invoke(prompt)
    return response.content

@tool
def generate_XML() -> str:
    """Generate synthetic data in XML format."""
    prompt = "Generate a synthetic dataset in an XML format with 10 fake user records. Include name, age, and email for each record."
    response = llm.invoke(prompt)
    return response.content

#Save all synthetic data to a file
@tool
def save_to_file(content: str, filename: str) -> str:
    """Save contents to a file with the proper filename extentions."""
    with open(filename, 'w') as f:
        f.write(content)
    return f"Saved to {filename}"

tools = [generate_JSON, generate_CSV, generate_XML, save_to_file]

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


synthetic_dataset_agent = create_react_agent(model, tools)
query = "Generate a dataset with 5 records for each format: JSON, CSV, and XML. Save each dataset into a file with the proper filename extension."
response = synthetic_dataset_agent.invoke({"messages": [HumanMessage(content=query)]})
logger.info(response["messages"])
