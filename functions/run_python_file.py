import os 
import subprocess

def run_python_file(working_directory: str, file_path: str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: '{file_path}' is not in this this working directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: '{file_path}' is not a file"  

    if not file_path.endswith(".py"):
        return f"Error {file_path} is not a python file" 

    try:
        output = subprocess.run(
            ["python3", file_path],
            cwd=abs_working_dir,
            timeout=30,  
            capture_output=True
        )
        final_string = f"""
        STDOUT: {output.stdout}
        STDERR: {output.stderr}
        """
        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
        return final_string
    except Exception as e:
        return f"Failed to run {file_path}, {e}"


schema_run_python_file = {
    "name": "run_python_file",
    "description": "Runs a Python file located within the specified working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file, relative to the working directory."
            }
        },
        "required": ["file_path"]
    }
}