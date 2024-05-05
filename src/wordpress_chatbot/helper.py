import os
from wordpress_chatbot import logger
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

def load_api_key(llm_provider):
    """
    Load the API key for the specified Large Language Model (LLM) provider from the environment variables.
    The supported LLM providers and their corresponding environment variable names are as follows:
        - OpenAI: "OPENAI_API_KEY"
        - GoogleAI: "GOOGLE_API_KEY"

    Args:
        llm_provider (str): The name of the LLM provider. Supported values: "OpenAI" or "GoogleAI".

    Returns:
        str: The API key for the specified LLM provider.

    Raises:
        ValueError: If the specified LLM provider is not supported or if the required environment variable is not set.
    """
    # Define environment variable names for different LLM providers
    llm_env_vars = {
        "OpenAI": "OPENAI_API_KEY",
        "GoogleAI": "GOOGLE_API_KEY"
    }

    # Check if the llm_provider is valid
    if llm_provider not in llm_env_vars:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    # Get the environment variable name for the given llm_provider
    env_var_name = llm_env_vars[llm_provider]

    # Check if the environment variable exists
    if env_var_name not in os.environ:
        raise ValueError(f"Environment variable {env_var_name} not found")

    # Get the API key from the environment variable
    api_key = os.getenv(env_var_name)

    return api_key
