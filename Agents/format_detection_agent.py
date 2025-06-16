import os
import time
import boto3
import logging
from pathlib import Path
import boto3
import datetime
from botocore.session import get_session
from botocore.credentials import RefreshableCredentials
from langchain_aws import ChatBedrockConverse
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ARN of Role A to assume  
role_to_assume = '[INSERT ARN HERE]'

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

region: str = "us-west-2"

# ---- ⚠️ Update region for your AWS setup ⚠️ ----
bedrock_client = boto3_session.client("bedrock-runtime",
                              region_name=region)

llm = ChatBedrockConverse(
    client=bedrock_client,
    model_id="us.amazon.nova-micro-v1:0",
    #model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0"
)

logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Format Detection Tool
@tool
def detect_file_format(file_path: str) -> str:
    """
    Detect the file format using the file extension.
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        return "csv"
    elif ext == ".json":
        return "json"
    elif ext == ".xml":
        return "xml"
    else:
        return f"unknown format ({ext})"


#Create prompt to ask LLM to detect format
path = "[INSERT PATH OF FOLDER WITH ALL FILES]"

query = f"""
You are a helpful data assistant. Your job is to detect the format of each file in the folder path (CSV, JSON, or XML).

Use the available tools instead of guessing.

When given a file path:
1. Detect the format using the file extension.
2. Return with a response that gives the file extension name in the following formats: .csv, .json or .xml. 
3. Be concise in your final answer.

The file is located at {path}
"""

#Create LLM pipeline 
model = init_chat_model("us.amazon.nova-micro-v1:0",
                        model_provider="bedrock_converse",
                        region_name="us-east-1",
                        client=bedrock_client)

tools = detect_file_format

agent_executor = create_react_agent(model, tools)

response = agent_executor.invoke({"messages": [HumanMessage(content=query)]})
logger.info(response["messages"])

Path("file_formats.txt").write_text(response["messages"][-1].content)
