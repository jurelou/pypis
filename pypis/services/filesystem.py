import os


def create_file_and_parents(file_path: str) -> None:
    """Create a file and all the parents directories."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
