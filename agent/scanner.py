import os
import pathlib
from typing import Dict, List

IGNORE_DIRS = {"target", ".git", ".settings", ".vscode", "test", "bin", "build"}


def scan_java_project(base_path: str):
    """
    This function walks through the given base path and scans for Java files,
    """
    found_files = []
    abs_base = os.path.abspath(base_path)
    for current_root, dirs, files in os.walk(abs_base):
        # skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        # Check for Java files
        for file_name in files:
            if file_name.endswith(".java"):
                # Construct full file path
                full_path = os.path.join(current_root, file_name)
                found_files.append(full_path)
    return found_files


def read_file_contents(file_paths: str) -> str:
    """
    Reads the contents of a file specified by file_paths and returns the file contents as string.
    """
    try:
        with open(file_paths, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_paths}: {e}")
        return f"Error reading file {file_paths}: {e}"


if __name__ == "__main__":
    test_project_path = "./samples/legacy-app"
    print(f"--- SCANNING: {test_project_path} ---")
    java_files = scan_java_project(test_project_path)

    project_source_code = {}

    for path in java_files:
        content = read_file_contents(path)
        file_name = os.path.basename(path)
        project_source_code[file_name] = content

    for file_name, code in project_source_code.items():
        print(f"--- CONTENT OF : {file_name} ---")
        print(code[:50])
        print("\n\n")
