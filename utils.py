import os
import json
from pathlib import Path

def sanitize_and_validate_path(path):
    """
    Sanitize and validate the given path to prevent directory traversal attacks.
    """
    # Resolve the absolute path
    final_path = Path(path).resolve()

    # Ensure the path is within the allowed directory
    allowed_base_dir = Path("/allowed/base/directory").resolve()
    if not str(final_path).startswith(str(allowed_base_dir)):
        raise ValueError("Invalid path: Path traversal detected")

    return final_path

def save_todo_file(todo_data, file_path):
    """
    Save the todo data to a file, ensuring the path is sanitized and validated.
    """
    try:
        # Sanitize and validate the file path
        final_path = sanitize_and_validate_path(file_path)

        # Ensure the directory exists
        final_dir = final_path.parent
        final_dir.mkdir(parents=True, exist_ok=True)

        # Save the todo data to the file
        with open(final_path, 'w') as file:
            json.dump(todo_data, file, indent=4)

    except Exception as e:
        print(f"An error occurred while saving the todo file: {e}")

# Example usage
if __name__ == "__main__":
    todo_data = {
        "tasks": [
            {"id": 1, "task": "Buy groceries", "completed": False},
            {"id": 2, "task": "Read a book", "completed": True}
        ]
    }
    file_path = "/allowed/base/directory/todos/todo_list.json"
    save_todo_file(todo_data, file_path)