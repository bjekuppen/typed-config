from typed_config import BaseConfig, Setting
from typed_config.exceptions import RequiredError, UndefinedKeyError
import pytest

@pytest.fixture
def SimpleConfig():
    class SimpleConfig(BaseConfig):
        key1 = Setting(str, required=True)
        key2 = Setting(str) 
    return SimpleConfig

def test_simple_config_all_keys(SimpleConfig):
    raw_config = {"key1":"1", "key2":"2"}
    cfg = SimpleConfig(raw_config)
    assert cfg._config['key1'] == "1"
    assert cfg._config['key2'] == "2"

def test_simple_config_only_required_keys(SimpleConfig):
    raw_config = {"key1":"1"}
    cfg = SimpleConfig(raw_config)
    assert cfg._config['key1'] == "1"

def test_simple_config_required_key_not_provided(SimpleConfig):
    raw_config = {"key2":"2"}
    with pytest.raises(RequiredError):
        cfg = SimpleConfig(raw_config)

def test_simple_config_datacast(SimpleConfig):
    raw_config = {"key1":2, "key2":True}
    cfg = SimpleConfig(raw_config)
    assert cfg._config['key1'] == "2"
    assert cfg._config['key2'] == "True"

def test_simple_get_item(SimpleConfig):
    raw_config = {"key1":"1", "key2":"2"}
    cfg = SimpleConfig(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2'] == "2"

def test_simple_get_item_invalid_type(SimpleConfig):
    raw_config = {"key1":"1", "key2":"2"}
    cfg = SimpleConfig(raw_config)
    with pytest.raises(TypeError):
        cfg[1]

def test_simple_get_invalid_key(SimpleConfig):
    raw_config = {"key1":"1", "key2":"2", "key3":"3"}
    with pytest.raises(UndefinedKeyError):
        cfg = SimpleConfig(raw_config)
