import os


def get_md_file_count_in_folder(folder_path: str) -> int:
    """
    Count the number of .md files in a folder, including subfolders.
    Args:
        folder_path (str): The path to the folder.
    Returns:
        int: The count of .md files.
    """
    md_file_count = 0
    for root, _, files in os.walk(folder_path):
        md_file_count += sum(1 for file in files if file.endswith('.md'))
    return md_file_count


def sort_folders_by_md_file_count(folder_path: str) -> list:
    """
    Sort folders by the count of .md files within each, in descending order.
    Args:
        folder_path (str): The path to the main folder.
    Returns:
        list: A list of folder names, sorted by .md file count.
    """
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(
        os.path.join(folder_path, f))]
    folder_md_count = {folder: get_md_file_count_in_folder(
        os.path.join(folder_path, folder)) for folder in folders}
    sorted_folders = sorted(
        folder_md_count, key=folder_md_count.get, reverse=True)
    return sorted_folders
