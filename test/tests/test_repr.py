from typed_config import BaseConfig, Setting, SettingGroup, SettingList
import pytest

class Config(BaseConfig):
    key1 = Setting(str)

def test_repr_BaseConfig():
    config = Config(config={"key1":1})
    assert repr(config) == "Config(config={'key1': 1})"

def test_repr_Setting_1():
    setting = Setting(str)
    assert repr(setting) == "Setting(datacast=<class 'str'>, required=False)"

def test_repr_Setting_2():
    setting = Setting(int, required=True)
    assert repr(setting) == "Setting(datacast=<class 'int'>, required=True)"

def test_repr_SettingGroup_1():
    setting_group = SettingGroup(Config)
    assert repr(setting_group) == "SettingGroup(config=<class 'test_repr.Config'>, required=False)"

def test_repr_SettingGroup_2():
    setting_group = SettingGroup(Config, required=True)
    assert repr(setting_group) == "SettingGroup(config=<class 'test_repr.Config'>, required=True)"

def test_repr_SettingList():
    setting = Setting(str)
    setting_list = SettingList(setting)
    assert repr(setting_list) == "SettingList(setting=Setting(datacast=<class 'str'>, required=False))"