import pytest
from typed_config import BaseConfig, Setting
import os

@pytest.fixture
def Config():
    class Config(BaseConfig):
        key1 = Setting(int)
        key2 = Setting(str)
        key3 = Setting(bool)
    return Config

@pytest.fixture()
def simple_config_yaml_path():
    return os.path.join(os.path.dirname(__file__), "test_configs", "yaml", "simple_config.yaml")

@pytest.fixture()
def simple_config_json_path():
    return os.path.join(os.path.dirname(__file__), "test_configs", "json", "simple_config.json")


def test_load_json(Config, simple_config_json_path):
    cfg = Config.load_json(simple_config_json_path)
    assert cfg["key1"] == 1
    assert cfg["key2"] == "2"
    assert cfg["key3"] == True

def test_load_yaml(Config, simple_config_yaml_path):
    cfg = Config.load_yaml(simple_config_yaml_path)
    assert cfg["key1"] == 1
    assert cfg["key2"] == "2"
    assert cfg["key3"] == True