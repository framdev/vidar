import os
import pytest
from vidar.internal import _set_environment_variables, _read_and_parse_dotenv_file, _file_exists
from vidar import load_dotenv_file


@pytest.fixture
def dotenv_file(tmp_path):
    file_content = "\n".join([
        "VAR_A=A",
        "VAR_B=B",
        "VAR_C=C",
    ])

    target_output = os.path.join(tmp_path,".env")
    with open(target_output, "w+") as f:
        f.write(file_content)

    return target_output


def test_file_exists(dotenv_file):
    assert _file_exists(dotenv_file) == True


def test_dotenv_file_not_set(dotenv_file):
    load_dotenv_file(path=dotenv_file, set_env_vars=False)

    assert os.environ.get("VAR_A", None) is None
    assert os.environ.get("VAR_B", None) is None
    assert os.environ.get("VAR_C", None) is None


def test_dotenv_file_set(dotenv_file):
    load_dotenv_file(path=dotenv_file)

    assert os.environ["VAR_A"] == "A"
    assert os.environ["VAR_B"] == "B"
    assert os.environ["VAR_C"] == "C"


def test_dotenv_file_return(dotenv_file):
    variables = load_dotenv_file(path=dotenv_file)

    assert variables["VAR_A"] == "A"
    assert variables["VAR_B"] == "B"
    assert variables["VAR_C"] == "C"


def test_read_and_parse_dotenv_file(dotenv_file):
    variables = _read_and_parse_dotenv_file(dotenv_file)

    assert variables["VAR_A"] == "A"
    assert variables["VAR_B"] == "B"
    assert variables["VAR_C"] == "C"


def test_set_environment_variables():
    env_vars = {
        "VAR_A": "A",
        "VAR_B": "B",
        "VAR_C": "C"
    }
    
    _set_environment_variables(env_vars)

    assert os.environ["VAR_A"] == env_vars["VAR_A"]
    assert os.environ["VAR_B"] == env_vars["VAR_B"]
    assert os.environ["VAR_C"] == env_vars["VAR_C"]