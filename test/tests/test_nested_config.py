from typed_config import BaseConfig, Setting, SettingGroup
from typed_config.exceptions import RequiredError
import pytest

@pytest.fixture
def NestedNestedConfig():
    class NestedNestedConfig(BaseConfig):
        key1 = Setting(str, required=True)
        key2 = Setting(str) 
    return NestedNestedConfig

@pytest.fixture
def NestedConfig(NestedNestedConfig):
    class NestedConfig(BaseConfig):
        key1 = Setting(str, required=True)
        key2 = Setting(str) 
        key3 = SettingGroup(NestedNestedConfig, required=True)
    return NestedConfig

@pytest.fixture
def Config(NestedConfig):
    class Config(BaseConfig):
        key1 = Setting(str, required=True)
        key2 = SettingGroup(NestedConfig)
    return Config

def test_nested_config_all_keys(Config):
    raw_config = {
                    "key1":"1", 
                    "key2": {
                        "key1":"2", 
                        "key2":"3",
                        "key3":{
                            "key1":"4",
                            "key2":"5"
                            }
                        }
                    }
    cfg = Config(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2']["key1"] == "2"
    assert cfg['key2']["key2"] == "3"
    assert cfg['key2']["key3"]["key1"] == "4"
    assert cfg['key2']["key3"]["key2"] == "5"

def test_nested_config_only_required_1(Config):
    raw_config = {
                    "key1":"1", 
                }
    cfg = Config(raw_config)
    assert cfg['key1'] == "1"

def test_nested_config_only_required_2(Config):
    raw_config = {
                    "key1":"1", 
                    "key2": {
                        "key1":"2", 
                        "key3":{
                            "key1":"3",
                            }
                        }
                    }
    cfg = Config(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2']["key1"] == "2"
    assert cfg['key2']["key3"]["key1"] == "3"

def test_nested_config_datacast(Config):
    raw_config = {
                    "key1":1, 
                    "key2": {
                        "key1":2, 
                        "key2":True,
                        "key3":{
                            "key1":4,
                            "key2":5
                            }
                        }
                    }
    cfg = Config(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2']["key1"] == "2"
    assert cfg['key2']["key2"] == "True"
    assert cfg['key2']["key3"]["key1"] == "4"
    assert cfg['key2']["key3"]["key2"] == "5"

def test_nested_config_required_1(Config):
    raw_config = {
                    "key1":"1", 
                    "key2": {
                        "key1":"2", 
                        "key2":"3",
                        }
                    }
    with pytest.raises(RequiredError):
        cfg = Config(raw_config)

def test_nested_config_required_2(Config):
    raw_config = {
                    "key1":"1", 
                    "key2": {
                        "key1":"2", 
                        "key2":"3",
                        "key3": {
                                "key2":"4"
                            }
                        }
                    }
    with pytest.raises(RequiredError):
        cfg = Config(raw_config)