import os 

def get_files_info(working_directory: str, directory: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    print(abs_working_dir)

    if directory is None:
        directory = working_directory
    abs_directory = os.path.join(abs_working_dir, directory)
    print(abs_directory)

    print(directory)
    if not abs_directory.startswith(abs_working_dir):
        return f"Error: '{directory}' is not a directory"

    final_response = ""
    contents = []
    if os.path.isdir(abs_directory):
        contents = os.listdir(abs_directory)
    print(contents)
    for content in contents:
         content_file = os.path.join(abs_directory, content)
         is_dir = os.path.isdir(content_file)
         size = os.path.getsize(content_file)
 
         final_response += f"- {content}: file-size={size} bytes, is_dir={is_dir}"
    return final_response

schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory path relative to the working directory. Defaults to the working directory itself."
            }
        },
        "required": ["directory"]
    }
}