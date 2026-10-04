from functions.write_file import write_file
from functions.run_python_file import run_python_file
def main():
    working_directory = "calculator"
    print(run_python_file(working_directory, "main.py"))

main() 