import os

def write_file(working_directory: str, file_path: str, content: str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f' file "{file_path}" does not exist'
    print(abs_file_path)
    if not os.path.isfile(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        print(parent_dir) 
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
           return  f"Could not creat a parent dirs: {parent_dir} = {e}"
    try:
        way = ""
        if os.path.isfile(abs_file_path):
            with open(abs_file_path, "r") as f:
                if f.read():
                    way = "a"
                else:
                    way = "w"
        else:
            way = "w"
        with open(abs_file_path, way) as f:
            f.write(f"{content}\n")
        return f'Successfully wrote to {file_path}, {len(content)} characters'
    except Exception as e:
        return f"Failed to write to the file {file_path}, {e}"



schema_write_file = {
    "name": "write_file",
    "description": "Writes content to a file within the specified working directory. Creates the file and parent directories if they do not exist.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path of the file relative to the working directory."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file."
            }
        },
        "required": [
            "file_path",
            "content"
        ]
    }
}