"""Entry point for command line tools enables via `python -m vidar`"""
import argparse
import os
import sys
import importlib
from .lib import BaseEnvironment
from .cli import create_or_update_dotenv_file

parser = argparse.ArgumentParser(prog='vidar', description='Utility cli to generate a .env file from a envrionment config class')
parser.add_argument('-i', '--input', help="File path to config class module")
parser.add_argument('-cn', '--classname', help="BaseEnvironment class name")
parser.add_argument('-o', '--output', help="Optional output path for the generated .env file (default: cwd)")
parser.add_argument('-p', '--prefix', help="Optional prefix for the environemnt variables in the .env file (default: empty)")


def _load_environment_class(module_path: str, class_name: str) -> BaseEnvironment:
    """Loads a BaseEnvironment class from a file path to a .py file"""
    module_name = os.path.basename(module_path).split(".")[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


if __name__ == "__main__":
    dotenv_file_name = ".env"
    output_path = os.path.join(os.getcwd(), dotenv_file_name)
    prefix = ""
    args = parser.parse_args()

    if args.input is None or args.classname is None:
        sys.exit("Input (-i) and Class name (-cn) is required")

    if args.output != None:
        output_path = os.path.join(os.getcwd(), args.output, dotenv_file_name)

    if args.prefix != None:
        prefix = args.prefix

    try:
        cls = _load_environment_class(os.path.join(os.getcwd(), args.input), args.classname)
        create_or_update_dotenv_file(cls, output_path, prefix)
    except:
        print(f"Could not load BaseEnvironment class {args.classname} at {os.path.join(os.getcwd(), args.input)}")
        print("Please check that the input path and class name is correct")
