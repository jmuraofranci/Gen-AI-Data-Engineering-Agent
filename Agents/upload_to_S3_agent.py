@tool
def upload_to_s3(local_path: str, bucket: str, s3_prefix: str) -> str:
    """
    Upload a local file to an S3 bucket under the specified prefix.
    """
    try:
        s3 = boto3.client("s3")
        s3_key = f"{s3_prefix}/{local_path.split('/')[-1]}"
        s3.upload_file(local_path, bucket, s3_key)
        return f"Uploaded {local_path} to s3://{bucket}/{s3_key}"
    except Exception as e:
        return f"Upload failed: {e}"


tools = [upload_to_s3]
s3_agent = create_react_agent(model, tools)
