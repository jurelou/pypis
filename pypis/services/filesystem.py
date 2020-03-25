import os


def create_file_and_parents(file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

