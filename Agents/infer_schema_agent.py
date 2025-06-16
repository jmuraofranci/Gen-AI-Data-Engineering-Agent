import pandas as pd
import json
import xml.etree.ElementTree as ET

#Schema Inference Tool
@tool
def detect_schema(file_path: str) -> str:
    """
    Inspect a CSV, JSON, XML, or Parquet file and return the detected schema (columns and types).
    """
    ext = Path(file_path).suffix.lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
            schema = {}
            for col in df.columns:
                schema[col] = str(df[col].dtype)
            return json.dumps(schema)

        elif ext == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)

            if isinstance(data, list):
                sample = data[0]
            else:
                sample = data

            schema = {}
            for key in sample:
                schema[key] = type(sample[key]).__name__

            return json.dumps(schema)

        elif ext == ".xml":
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            #This uses recursion to search through the XML tree
            def extract_xml_schema(element, parent_path=""):
                schema = {}
v
                    if child.text and child.text.strip():
                        schema[child_path] = type(child.text.strip()).__name__

                    child_schema = extract_xml_schema(child, child_path)
                    schema.update(child_schema)

                return schema

            schema = extract_xml_schema(root)
            return json.dumps(schema)

    except Exception as e:
        return f"Error during schema detection: {str(e)}"

#Create prompt to ask LLM to detect format
path = "[INSERT PATH OF FOLDER WITH ALL FILES]"

query = f"""
You are a helpful data assistant. Your job is to understand the files in the folder path and extract their schema (columns, keys, and data types).

Use the available tools instead of guessing.

When given a file path:
1. Look through each file carefully. The files will have the following file formats: .csv, .json or .xml. 
2. Infer the schema from the file contents in each file.
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

Path("schema.txt").write_text(response["messages"][-1].content)
