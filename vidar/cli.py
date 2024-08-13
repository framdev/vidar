import os
from .lib import BaseEnvironment
from .internal import _file_exists


def _read_dot_env_file(path: str) -> str:
    file_content = ""
    if _file_exists(path):
        with open(path, "r", encoding="UTF-8") as f:
            file_content = f.read()
    
    return file_content


def _get_environment_variables_from_class_sheama(env_cls: BaseEnvironment) -> dict[str, str]:
    """Gets the varaibles from the configuration class scheama and returns a dictionary"""
    schema_variables = {}
    schema = env_cls.model_json_schema()
    for key in schema["properties"].keys():
        schema_property = schema["properties"][key]
        schema_variables[key.upper()] = schema_property.get("default", "<value here>")
    
    return schema_variables


def create_or_update_dotenv_file(base_env_cls: BaseEnvironment, output_path: str, prefix: str = "") -> None:
    """Create or update a .env at output path from a configuration class"""
    dot_env_contents = _read_dot_env_file(output_path)
    schema_properties = _get_environment_variables_from_class_sheama(base_env_cls)

    with open(output_path, "a") as f:
        for prop in schema_properties:
            if f"{prop.upper()}=" not in dot_env_contents:
                f.write(f"{prefix.upper()}{prop.upper()}={schema_properties[prop]}{os.linesep}")

    print(f"file {output_path} has been updated")