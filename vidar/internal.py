import os
from pathlib import Path


def _file_exists(path: str) -> bool:
    """Checks if a file at a give path exists"""
    return Path(path).exists()


def _get_dot_env_path(path: str) -> str | None:
    """Checks the if .env file exists at a given path or in the current och parent direcotry of cwd"""
    dot_env_path = None
    dot_env_file_name = ".env"
    cwd = os.getcwd()
    path_current_dir = os.path.join(os.path.abspath(Path(cwd).resolve()), dot_env_file_name)
    path_parent_dir = os.path.join(os.path.abspath(Path(cwd).resolve().parent),  dot_env_file_name)

    if path and Path(path).exists():
        dot_env_path = path
    elif _file_exists(path_current_dir):
        dot_env_path = path_current_dir
    elif _file_exists(path_parent_dir):
        dot_env_path = path_parent_dir

    return dot_env_path

def _set_environment_variables(environment_variables: dict[str, str]) -> None:
    """Sets environment variables from a dictionary"""
    for key in environment_variables:
        os.environ[key] = environment_variables[key]


def _read_and_parse_dotenv_file(file_path: str) -> dict[str, str]:
    """
    Reads  and parses a .env file at a given file path and
    returns dictionary with key values of the contents of the file
    """
    dotenv_variables = {}
    with open(file_path, "r", encoding="UTF-8") as file:
        while line := file.readline():
            # Lines beginning with # is comments and should be skipped
            if line.startswith("#"):
                continue

            values = line.strip().split("=", 1)
            if len(values) == 2 and values[1] != '':
                dotenv_variables[values[0].upper()] = values[1]
    
    return dotenv_variables
