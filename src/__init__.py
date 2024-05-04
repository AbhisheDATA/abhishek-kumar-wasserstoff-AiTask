import os
import sys
import logging
from pathlib import Path

# path for the congif yaml file 
CONFIG_FILE_PATH = Path("config/config.yaml")

def setup_logger():
    """
    Set up logging configuration.

    Configure logging to output logs both to a file and to the console.

    Returns:
        logging.Logger: The logger object.
    """
    logging.info("Setting up logging")
    # Define logging format
    logging_format = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

    # Define log directory and file path
    log_dir = "logs"
    log_filepath = os.path.join(log_dir, "running_logs.log")

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Get logger object
    logger = logging.getLogger("RAG_ChatbotLogger")
    return logger

# Call setup_logger to set up logging
logger = setup_logger()
