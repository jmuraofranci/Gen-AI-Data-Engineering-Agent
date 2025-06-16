from pydantic import BaseModel, create_model
import pandas as pd
import json
import csv
import xml.etree.ElementTree as ET
from io import BytesIO
from typing import List
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

@tool
def json_to_parquet_with_pydantic(schema_json: dict, data_json: list, output_path: str) -> str:
    """
    Generates a Pydantic model from a JSON schema, validates the input data, and writes it to a Parquet file.
    """
    try:
        fields = {k: (eval(v), ...) if isinstance(v, str) else (str, ...) for k, v in schema_json.items()}
        DynamicModel = create_model("DynamicModel", **fields)

        validated_data = [DynamicModel(**item).model_dump() for item in data_json]
        df = pd.DataFrame(validated_data)
        df.to_parquet(output_path, index=False)

        return f"Parquet file written to {output_path}"
    except Exception as e:
        return f"Error: {e}"
@tool
def csv_to_parquet_with_pydantic(schema_json: dict, csv_data: str, output_path: str) -> str:
    """
    Converts CSV data to Parquet using a Pydantic model generated from the schema.
    """
    try:

        df = pd.read_csv(pd.compat.StringIO(csv_data))
        
        fields = {k: (eval(v), ...) if isinstance(v, str) else (str, ...) for k, v in schema_json.items()}
        DynamicModel = create_model("DynamicModel", **fields)
        
        validated_data = [DynamicModel(**row).model_dump() for _, row in df.iterrows()]
        df = pd.DataFrame(validated_data)
        df.to_parquet(output_path, index=False)

        return f"Parquet file written to {output_path}"
    except Exception as e:
        return f"Error: {e}"

@tool
def xml_to_parquet_with_pydantic(schema_json: dict, xml_data: str, output_path: str) -> str:
    """
    Converts XML data to Parquet using a Pydantic model generated from the schema.
    """
    try:
        root = ET.fromstring(xml_data)
        data = []
        for item in root:
            row = {child.tag: child.text for child in item}
            data.append(row)

        fields = {k: (eval(v), ...) if isinstance(v, str) else (str, ...) for k, v in schema_json.items()}
        DynamicModel = create_model("DynamicModel", **fields)

        validated_data = [DynamicModel(**item).model_dump() for item in data]
        df = pd.DataFrame(validated_data)
        df.to_parquet(output_path, index=False)

        return f"Parquet file written to {output_path}"
    except Exception as e:
        return f"Error: {e}"


tools = [
    json_to_parquet_with_pydantic,
    csv_to_parquet_with_pydantic,
    xml_to_parquet_with_pydantic,
]

pydantic_parquet_agent = create_react_agent(model, tools)
