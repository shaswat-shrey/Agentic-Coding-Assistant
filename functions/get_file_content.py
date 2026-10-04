import os
from config import MAX_CHARS

def get_file_content(working_directory: str, filepath: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, filepath))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: '{filepath}' is not in this this working directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: '{filepath}' is not a file" 

    file_content_string = ""
    with open(abs_file_path, 'r') as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) >= MAX_CHARS:
            file_content_string += (
                f" ...File '{filepath}' is truncated to max 10,000 Characters"
            )

    return file_content_string


schema_get_file_content = {
    "name": "get_file_content",
    "description": "Reads the contents of a file within the specified working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "The path to the file, relative to the working directory."
            }
        },
        "required": ["filepath"]
    }
}