import os


def md_file_count(folder_path: str) -> int:
    """
    Get the number of .md files in each folder.
        Args:
            folder_path (str): Path to the folder
        Returns:
            int: Total number of .md files in the folder
    """
    # Get a list of folders within the specific folder
    folder_list = [f for f in os.listdir(
        folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Initialize a variable to store the total number of .md files
    result = 0

    for folder in folder_list:
        folder_dir = os.path.join(folder_path, folder)
        for _, _, files in os.walk(folder_dir):
            for file in files:
                if file.endswith(".md"):
                    result += 1

    return result


def sort_folders(folder_path: str) -> list:
    """
    Sort the folder names based on .md file counts in descending order.
        Args:
            folder_path (str): Path to the folder
        Returns:
            list: List of sorted folder names
    """
    # Get a list of folders within the specific folder
    folder_list = [f for f in os.listdir(
        folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Initialize a dictionary to store folder names and their respective .md file counts
    md_file_counts = {}

    for folder in folder_list:
        folder_dir = os.path.join(folder_path, folder)
        md_file_counts[folder] = md_file_count(folder_dir)

    # Sort the folder names based on .md file counts in descending order
    sorted_folders = sorted(
        md_file_counts, key=lambda x: md_file_counts[x], reverse=True)

    return sorted_folders
