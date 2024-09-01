# vidar
Environment variables with Python type hints using [Pydantic](https://docs.pydantic.dev/latest/)

### Getting Started
```shell
pip install git+https://github.com/framdev/vidar
```

```bash
# example .env file
DEBUG=True
SECRET_KEY=$3C2E7_K3Y
```


```python
from vidar import BaseEnvironment


class Environment(BaseEnvironment):
    debug: bool = False
    secret_key: str


env = Environment.load()
print(env.secret_key)
```

Environment variables will be loaded from the system environment variables and a optional .env file in the current working directory or the parent directory of the script.


The environment variables in the loaded ```.env``` file will not be set in to the ```os.environ``` dictionary when the load method is used. To add the environment variables from the loaded ```.env``` file to the ```os.environ``` dictionary set the ```set_env_vars```flag to True.

```python
env = Environment.load(set_env_vars=True)
```

To change the path of the .env file use the path parameter
```python
env = Environment.load(path="PATH_TO_DOT_ENV_FILE")
```

vidar can also be used to just load a ```.env``` file in to the ```os.environ``` dictionary via the ```load_dotenv_file``` function
```python
import os
from vidar import load_dotenv_file


load_dotenv_file(path="PATH_TO_DOT_ENV_FILE")
print(os.environ['SECRET_KEY'])
```

### CLI Usage
vidar exposes a command line interface to generate or update an existing ```.env``` file from a ```BaseEnvironment``` class
```bash
python -m vidar -i ./path/to/module.py -cn BASE_ENVIRONMENT_CLASS_NAME
```

the ```.env``` file will be written to the current working directory by default to change the output path use the ```-o``` flag

```bash
python -m vidar -i ./path/to/module.py -cn BASE_ENVIRONMENT_CLASS_NAME -o ./output/path
```