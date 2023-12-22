from typed_config import BaseConfig, Setting, SettingList
from typed_config.exceptions import RequiredError
import pytest

@pytest.fixture
def ListedConfig():
    class ListedConfig(BaseConfig):
        key1 = Setting(str, required=True)
        key2 = SettingList(Setting(str))
        key3 = SettingList(Setting(str, required=True))
    return ListedConfig

def test_listed_config_all_keys(ListedConfig):
    raw_config = {
                    "key1":"1", 
                    "key2": ["2"],
                    "key3": ["3", "4"]
                }
                        
    cfg = ListedConfig(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2'] == ["2"]
    assert cfg['key3'] == ["3", "4"]

def test_listed_config_only_required_keys(ListedConfig):
    raw_config = {
                    "key1":"1", 
                    "key3": ["3", "4"]
                }
    cfg = ListedConfig(raw_config)
    assert cfg._config['key1'] == "1"

def test_simple_config_required_key_not_provided(ListedConfig):
    raw_config = {
                    "key1":"1", 
                    "key2": ["2"],
                }
    with pytest.raises(RequiredError):
        cfg = ListedConfig(raw_config)

def test_simple_config_datacast(ListedConfig):
    raw_config = {
                    "key1":1, 
                    "key2": [2],
                    "key3": [3, True]
                }
    cfg = ListedConfig(raw_config)
    assert cfg['key1'] == "1"
    assert cfg['key2'] == ["2"]
    assert cfg['key3'] == ["3", "True"]