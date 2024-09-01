""" Vidar: Environment variables with Python type hints """
from .lib import BaseEnvironment as BaseEnvironment
from .lib import load_dotenv_file as load_dotenv_file

__version__ = "1.0.0-beta"
__all__ = ['load_dotenv_file', 'BaseEnvironment']