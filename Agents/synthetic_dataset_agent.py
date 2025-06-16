@tool
def generate_JSON() -> str:
    """Generate synthetic data in JSON format."""
    prompt = """Generate a synthetic dataset in a JSON array with 10 fake user records. 
Each record must include fields: name, age, and email. 
Format the output as a valid JSON array (with correct indentation and no extra text)."""
    response = nova_model.invoke(prompt)
    return response.content

@tool
def generate_CSV() -> str:
    """Generate synthetic data in CSV format."""
    prompt = """Generate a synthetic dataset in CSV format with 10 fake user records.
Include columns: name, age, and email. 
Return only the CSV contents (no explanation text). 
Make sure the CSV is properly formatted with headers on the first row."""
    response = nova_model.invoke(prompt)
    return response.content

@tool
def generate_XML() -> str:
    """Generate synthetic data in XML format."""
    prompt = """Generate a synthetic dataset in XML format with 10 fake user records.
Each record must include fields: name, age, and email. 
Wrap all records under a root <records> element. 
Ensure valid XML structure with proper nesting and indentation. Return only the XML."""
    response = nova_model.invoke(prompt)
    return response.content


#Save all synthetic data to a file
@tool
def save_to_file(content: str, filename: str) -> str:
    """Save contents to a file with the proper filename extensions."""
    # Define and create the output directory
    data_dir = Path("generated_data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file
    filepath = data_dir / filename
    with open(filepath, 'w') as f:
        f.write(content)
    
    return f"Saved to {filepath}"


data_generation_tools = [generate_JSON, generate_CSV, generate_XML, save_to_file]
data_generation_agent = create_react_agent(model, data_generation_tools)

#Write prompt to generate sythetic dataset 
synthetic_dataset_agent = create_react_agent(model, tools)
query = "Generate a dataset with 10 records for each format: JSON, CSV, and XML. Save each dataset into a file with the proper filename extension."
response = synthetic_dataset_agent.invoke({"messages": [HumanMessage(content=query)]})
logger.info(response["messages"])
