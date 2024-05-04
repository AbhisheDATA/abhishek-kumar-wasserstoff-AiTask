import os
import logging
from pathlib import Path

# Decorator function to log function calls
def log_function_call(func):
    """
    Decorator to log function calls.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Decorator function to set up logging
def setup_logger():
    """
    Set up logging configuration.

    Returns:
        logging.Logger: The logger object.
    """
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')
    return logging.getLogger(__name__)

# Call setup_logger to set up logging
logger = setup_logger()

# List of directories to create if not exist
list_of_directories = [
    "Data/docs",
    "Data/temp"
]

# List of files to create if not exist
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/component/__init__.py",
    "src/component/RAG_Chatbot.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "requirements.txt",
    "config/config.yaml"
]

@log_function_call
def create_directories_and_files():
    """
    Create directories and files if they do not exist.

    This function iterates over the list of directories and files
    specified at the beginning of the script and creates them if
    they do not already exist. It also logs the creation process.
    """
    # Create directories if they do not exist
    for directory in list_of_directories:
        directory = Path(directory)

        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Creating directory: {directory}")

    # Create files if they do not exist or are empty
    for filepath in list_of_files:
        filepath = Path(filepath)

        filedir = filepath.parent
        if not filedir.exists():
            filedir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Creating directory: {filedir}")

        if not filepath.exists() or os.path.getsize(filepath) == 0:
            with open(filepath, 'w') as f:
                logger.info(f"Creating empty file: {filepath}")
        else:
            logger.info(f"{filepath.name} already exists")

# Execute function to create directories and files
create_directories_and_files()