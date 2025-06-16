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
Esnure you install uv and Python dependencies:
1. Open a Terminal and run the following command to install uv.
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```
2. Clone the repo for which this installation is being done. cd into that repo.
```sh
git clone https://github.com/path/to/your-repo
cd your-repo
```
3. Restore Python virtual environment from the pyproject.toml file.
```sh
uv venv && source .venv/bin/activate && uv pip install --requirement pyproject.toml
```
4. Create a conda kernel.
```sh
uv add zmq
python -m ipykernel install --user --name=.venv --display-name="Python (uv env)"
```
5. Setup your Amazon Bedrock cross-account access (this is not related to uv but just one of the steps we need to get operational).
```sh
echo "arn:aws:iam:::..........." > ${HOME}/BedrockCrossAccount.txt
```
6. Open the JupyterLab notebook to run and select the Python (uv env) if not selected automatically (if it is not, refresh the page or close the notebook and open it again and you should see it selected or be able to select it from the drop down).

## Output
- Schema-inferred datasets in a standardized format
- Serialized and validated data ready for machine learning and analytics
- Partitioned storage for optimized querying

  
