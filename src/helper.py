import os
from src import logger
from box.exceptions import BoxValueError
from box import ConfigBox
import yaml
from pathlib import Path

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

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    