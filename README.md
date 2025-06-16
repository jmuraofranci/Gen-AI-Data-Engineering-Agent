# Gen-AI-Data-Engineering-Agent-Automating-Schema-Inference-and-Format-Conversion

## Overview
The GenAI-Powered Data Engineering Agent is a fully autonomous agent that builds data pipelines to automate schema inference, data format detection, serialization, and transformation. It recognizes file types (JSON, CSV, XML) and extracts schemas. It also generates Python code that actively standardizes, cleans, and stores data.

## Features
- Detects JSON, CSV, adn XML formats in local/S3 storage
- Extracts and infers schemas including nested structures and missing values
- Generates Python serialization/deserialization classes using GenAI
- Transforms and standardizes data into Parquet for analytics and Avro for streaming
- Automates schema-based partitioning, cleaning, and validation using Pydantic
- Supports multi-agent orchestration for execution and automation

## Installation
Ensure you have Python installed, then install dependencies:
```sh
pip install pydantic boto3 langchain faiss-cpu
```

## Usage
Run the script from the command line:
```sh
python main.py --input_path <path_to_data> --output_path <path_to_output>
```
Example:
```sh
python main.py --input_path data/ --output_path transformed_data/
```

## Output
- Schema-inferred datasets in a standardized format
- Serialized and validated data ready for machine learning and analytics
- Partitioned storage for optimized querying

  
