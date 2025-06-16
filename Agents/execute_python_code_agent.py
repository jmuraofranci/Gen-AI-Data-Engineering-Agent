@tool
def execute_generated_code(filename: str = "generated_data/generated_pipeline.py") -> str:
    """Execute the generated code."""
    try:
        with open(filename, "r") as f:
            code = f.read()
        exec(code, globals())
        return "Successfully executed the code."
    except Exception as e:
        return f"Failed to execute: {e}"

tools = [execute_generated_code]
code_execution_agent = create_react_agent(model, tools)
