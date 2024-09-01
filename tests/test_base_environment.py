import os
import pytest
from vidar import BaseEnvironment

@pytest.fixture
def dot_env_file(tmp_path):
    file_content = "\n".join([
        "BOOLEAN=True",
        "TEXT=text",
        "NUMBER=1"
    ])

    target_output = os.path.join(tmp_path,".env")
    with open(target_output, "w+") as f:
        f.write(file_content)

    return target_output


@pytest.fixture
def dot_env_file_prefix(tmp_path):
    file_content = "\n".join([
        "PREFIX_TEXT=text",
    ])

    target_output = os.path.join(tmp_path,".env")
    with open(target_output, "w+") as f:
        f.write(file_content)

    return target_output


@pytest.fixture
def dot_env_file_list(tmp_path):
    file_content = "\n".join([
        "LIST=item1:item2:item3",
    ])

    target_output = os.path.join(tmp_path,".env")
    with open(target_output, "w+") as f:
        f.write(file_content)

    return target_output


def test_configuration_class_loading(dot_env_file):
    class TestConfig(BaseEnvironment):
        boolean: bool
        text: str
        number: int

    env = TestConfig.load(path=dot_env_file)

    assert env.boolean == True
    assert env.text == "text"
    assert env.number == 1


def test_configuration_class_data_types(dot_env_file):
    class TestConfig(BaseEnvironment):
        boolean: bool
        text: str
        number: int

    env = TestConfig.load(path=dot_env_file)

    assert type(env.boolean) is bool
    assert type(env.text) is str
    assert type(env.number) is int


def test_configuration_class_defaults(dot_env_file):
    class TestConfig(BaseEnvironment):
        text: str = "default text"
        default: str = "default"

    env = TestConfig.load(path=dot_env_file)

    assert env.text == "text"
    assert env.default == "default"


def test_configuration_class_environment_variables_are_set(dot_env_file):
    class TestConfig(BaseEnvironment):
        text: str = "text"

    env = TestConfig.load(path=dot_env_file, set_env_vars=True)
    
    assert env.text == "text"
    assert os.environ["TEXT"] == "text"


def test_configuration_class_outside_variable(dot_env_file):
    os.environ["OUTSIDE"] = "outside"
    
    class TestConfig(BaseEnvironment):
        outside: str

    env = TestConfig.load(path=dot_env_file)

    assert env.outside == "outside"


def test_configuration_class_missing(dot_env_file):
    class TestConfig(BaseEnvironment):
        missing: str

    try:
        TestConfig.load(path=dot_env_file)
        assert False
    except Exception:
        assert True


def test_dotenv_with_prefix(dot_env_file_prefix):
    class PrefixConfigClass(BaseEnvironment):
        text: str


    env = PrefixConfigClass.load(path=dot_env_file_prefix, prefix="PREFIX_")

    assert env.text == "text"

def test_dotenv_with_list(dot_env_file_list):
    class ListConfigClass(BaseEnvironment):
        list: list


    env = ListConfigClass.load(path=dot_env_file_list, list_delimiter=":")

    assert len(env.list) == 3
    assert env.list[0] == "item1"
    assert env.list[1] == "item2"
    assert env.list[2] == "item3"
