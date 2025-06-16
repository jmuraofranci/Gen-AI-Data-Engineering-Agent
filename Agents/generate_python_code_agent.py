@tool
def save_generated_code(code: str, filename: str = "generated_pipeline.py") -> str:
    """
    Saves the generated code to a Python file.
    """
    try:
        with open(filename, "w") as f:
            f.write(code)
        return f"Code saved to {filename}"
    except Exception as e:
        return f"Failed to save code: {str(e)}"

tools = [save_generated_code]
code_generator_agent = create_react_agent(model, tools)
