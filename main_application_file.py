import os
import re
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to sanitize user inputs
def sanitize_input(user_input):
    return re.sub(r'[^\w\s-]', '', user_input)

# Function to validate paths
def is_valid_path(base_dir, path):
    try:
        # Resolve the absolute path and ensure it starts with the base directory
        return Path(path).resolve().startswith(Path(base_dir).resolve())
    except Exception as e:
        return False

@app.route('/create_todo', methods=['POST'])
def create_todo():
    data = request.json
    first_class = sanitize_input(data.get('first_class', ''))
    second_class = sanitize_input(data.get('second_class', ''))
    todo_title = sanitize_input(data.get('todo_title', ''))

    base_dir = '/safe_base_directory'
    final_dir = os.path.join(base_dir, first_class, second_class)

    if not is_valid_path(base_dir, final_dir):
        return jsonify({"error": "Invalid path"}), 400

    os.makedirs(final_dir, exist_ok=True)
    todo_file_path = os.path.join(final_dir, f"{todo_title}.txt")

    with open(todo_file_path, 'w') as todo_file:
        todo_file.write(f"Title: {todo_title}\n")

    return jsonify({"message": "TODO created successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)