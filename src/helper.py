import os
from src import logger

def create_directories(path_to_directories: list, verbose=True):
    """
    Create directories specified in the list.

    Args:
        path_to_directories (list): List of paths of directories to be created.
        verbose (bool, optional): Whether to log directory creation messages. Defaults to True.
    """
    for path in path_to_directories:
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Log directory creation if verbose mode is enabled
        if verbose:
            logger.info(f"Created directory at: {path}")
