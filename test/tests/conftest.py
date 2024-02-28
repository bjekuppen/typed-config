from typed_config import BaseConfig, Setting, SettingGroup, SettingList
import pytest

class NestedNestedConfig(BaseConfig):
    key1 = SettingList(Setting(str, required=True))
    key2 = SettingList(Setting(str))
    key3 = Setting(str)

class NestedConfig(BaseConfig):
    key1 = SettingList(SettingGroup(NestedNestedConfig, required=True))
    key2 = SettingList(SettingGroup(NestedNestedConfig))
    key3 = Setting(str)

class Config(BaseConfig):
    key1 = SettingGroup(NestedConfig, required=True)
    key2 = Setting(str) 

@pytest.fixture()
def raw_config():
    raw_config = {
                    "key1":{
                        "key1":[
                                {
                                "key1":["1", "2"],
                                "key2":["3", "4"],
                                "key3":"5"
                                },
                                {
                                "key1":["6", "7"],
                                "key2":["8", "9"],
                                "key3":"10"
                                }
                                ],
                        "key2":[
                                {
                                "key1":["11", "12"],
                                "key2":["13", "14"],
                                "key3":"15"
                                },
                                {
                                "key1":["16", "17"],
                                "key2":["18", "19"],
                                "key3":"20"
                                }
                                ],
                        "key3": "21"
                    }, 
                    "key2":"22"
                }
    return raw_config

@pytest.fixture
def example_config(raw_config):
    return Config(raw_config)