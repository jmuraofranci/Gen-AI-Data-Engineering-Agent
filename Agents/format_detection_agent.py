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
