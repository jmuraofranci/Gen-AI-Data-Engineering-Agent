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
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Setup logging
logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS Session Setup
ROLE_TO_ASSUME = Path(os.path.join(os.environ["HOME"], "BedrockCrossAccount.txt")).read_text().strip()
logger.info(f"ROLE_TO_ASSUME={ROLE_TO_ASSUME}")

def get_credentials():
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=ROLE_TO_ASSUME,
        RoleSessionName='cross-account-session',
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

bedrock_client = boto3_session.client("bedrock-runtime", region_name=region)

model = init_chat_model("us.anthropic.claude-3-5-haiku-20241022-v1:0",
                        model_provider="bedrock_converse",
                        region_name="us-east-1",
                        client=bedrock_client)

nova_model = init_chat_model("us.amazon.nova-micro-v1:0",
                        model_provider="bedrock_converse",
                        region_name="us-east-1",
                        client=bedrock_client)

data_dir = Path("generated_data")
data_dir.mkdir(exist_ok=True)
