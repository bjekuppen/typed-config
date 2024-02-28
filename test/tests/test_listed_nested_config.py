from typed_config import BaseConfig, Setting, SettingGroup, SettingList
from typed_config.exceptions import RequiredError
import pytest

@pytest.fixture
def NestedNestedConfig():
    class NestedNestedConfig(BaseConfig):
        key1 = SettingList(Setting(str, required=True))
        key2 = SettingList(Setting(str))
        key3 = Setting(str)
    return NestedNestedConfig

@pytest.fixture
def NestedConfig(NestedNestedConfig):
    class NestedConfig(BaseConfig):
        key1 = SettingList(SettingGroup(NestedNestedConfig, required=True))
        key2 = SettingList(SettingGroup(NestedNestedConfig))
        key3 = Setting(str)
    return NestedConfig

@pytest.fixture
def Config(NestedConfig):
    class Config(BaseConfig):
        key1 = SettingGroup(NestedConfig, required=True)
        key2 = Setting(str) 
    return Config

def test_nested_listed_config_all_keys(Config):
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
    cfg = Config(raw_config)
    assert cfg['key1']['key1'][0]['key1'] == ["1", "2"]
    assert cfg['key1']['key1'][0]['key2'] == ["3", "4"]
    assert cfg['key1']['key1'][0]['key3'] == "5"
    assert cfg['key1']['key1'][1]['key1'] == ["6", "7"]
    assert cfg['key1']['key1'][1]['key2'] == ["8", "9"]
    assert cfg['key1']['key1'][1]['key3'] == "10"

    assert cfg['key1']['key2'][0]['key1'] == ["11", "12"]
    assert cfg['key1']['key2'][0]['key2'] == ["13", "14"]
    assert cfg['key1']['key2'][0]['key3'] == "15"
    assert cfg['key1']['key2'][1]['key1'] == ["16", "17"]
    assert cfg['key1']['key2'][1]['key2'] == ["18", "19"]
    assert cfg['key1']['key2'][1]['key3'] == "20"

    assert cfg['key1']['key3'] == "21"

    assert cfg['key2'] == "22"


def test_nested_listed_config_only_required_1(Config):
    raw_config = {
                    "key1":{
                        "key1":[
                                {
                                "key1":["1", "2"],
                                },
                                {
                                "key1":["6", "7"],
                                }
                                ]
                    }, 
                }
    cfg = Config(raw_config)
    assert cfg['key1']['key1'][0]['key1'] == ["1", "2"]
    assert cfg['key1']['key1'][1]['key1'] == ["6", "7"]

def test_nested_listed_config_datacast(Config):
    raw_config = {
                "key1":{
                    "key1":[
                            {
                            "key1":[1, 2],
                            "key2":[3, 4],
                            "key3":5
                            },
                            {
                            "key1":[6, 7],
                            "key2":[False, 9],
                            "key3":10
                            }
                            ],
                    "key2":[
                            {
                            "key1":[11, True],
                            "key2":[13, 14],
                            "key3":15
                            },
                            {
                            "key1":[16, 17],
                            "key2":[18, 19],
                            "key3":True
                            }
                            ],
                    "key3": 21
                }, 
                "key2":False
            }
    cfg = Config(raw_config)
    assert cfg['key1']['key1'][0]['key1'] == ["1", "2"]
    assert cfg['key1']['key1'][0]['key2'] == ["3", "4"]
    assert cfg['key1']['key1'][0]['key3'] == "5"
    assert cfg['key1']['key1'][1]['key1'] == ["6", "7"]
    assert cfg['key1']['key1'][1]['key2'] == ["False", "9"]
    assert cfg['key1']['key1'][1]['key3'] == "10"

    assert cfg['key1']['key2'][0]['key1'] == ["11", "True"]
    assert cfg['key1']['key2'][0]['key2'] == ["13", "14"]
    assert cfg['key1']['key2'][0]['key3'] == "15"
    assert cfg['key1']['key2'][1]['key1'] == ["16", "17"]
    assert cfg['key1']['key2'][1]['key2'] == ["18", "19"]
    assert cfg['key1']['key2'][1]['key3'] == "True"

    assert cfg['key1']['key3'] == "21"

    assert cfg['key2'] == "False"

def test_nested_listed_config_required_1(Config):
    raw_config = {
                    "key1":{
                        "key2":[
                                {
                                "key1":["1", "2"],
                                }
                                ]
                    }, 
                }
    with pytest.raises(RequiredError):
        cfg = Config(raw_config)

def test_nested_listed_config_required_2(Config):
    raw_config = {
                    "key2":"22"
                }
    with pytest.raises(RequiredError):
        cfg = Config(raw_config)

def test_nested_lister_config_eq(Config):
    raw_config = {
                    "key1":{
                        "key1":[
                                {
                                "key1":["1", "2"],
                                },
                                {
                                "key1":["6", "7"],
                                }
                                ]
                    }, 
                }
    cfg = Config(raw_config)
    cfg2 = Config(raw_config)
    assert cfg == cfg2

def test_nested_lister_config_not_eq(Config):
    raw_config = {
                    "key1":{
                        "key1":[
                                {
                                "key1":["1", "2"],
                                },
                                {
                                "key1":["6", "7"],
                                }
                                ]
                    }, 
                }
    raw_config2 = {
                    "key1":{
                        "key1":[
                                {
                                "key1":["2", "2"],
                                },
                                {
                                "key1":["6", "7"],
                                }
                                ]
                    }, 
                }
    cfg = Config(raw_config)
    cfg2 = Config(raw_config2)
    assert not cfg == cfg2
