import os
from pydantic import BaseModel, ValidationError
from .internal import _read_and_parse_dotenv_file, _set_environment_variables, _get_dot_env_path


def load_dotenv_file(path: str = None, set_env_vars: bool = True) -> dict[str, str]:
    """Loads a .env file (cwd or parent as default) and sets the environment variables"""
    dotenv_vars = {}
    file_path = _get_dot_env_path(path)

    if file_path != None:
        dotenv_vars = _read_and_parse_dotenv_file(file_path)
    
    if set_env_vars:
        _set_environment_variables(dotenv_vars)
    
    return dotenv_vars


class BaseEnvironment(BaseModel):
    @classmethod
    def load(cls, path: str = None, prefix: str = "", set_env_vars: bool = False, list_delimiter: str = ","):
        """Loads environment variables from a .env file and returns a instance of the BaseEnvironment class (self)"""
        environment_variables = {}
        dot_env_variables = load_dotenv_file(path, set_env_vars = set_env_vars)
        properties = cls.model_json_schema()["properties"]

        for key in properties.keys():
            value = None
            schema_property = properties[key]
            variable_name = prefix.upper() + key.upper()
            variable = dot_env_variables.get(variable_name, schema_property.get("default", None))
            environment_variable = os.environ.get(variable_name, variable)
            
            if schema_property["type"] == "array":
                value = environment_variable.split(list_delimiter)
            else:
                value = environment_variable

            environment_variables[key] = value
        
        try:
            return cls(**environment_variables)
        except ValidationError as e:
            raise Exception(e)
