import pytest

from typed_config import BaseConfig, Setting
from typed_config import datacast

from enum import Enum, StrEnum

class EnumTest(Enum):
    a = 1
    b = 2

class StrEnumTest(StrEnum):
    a = "a"
    b = "b"


@pytest.fixture
def ConfigEnumTest():
    class ConfigEnumTest(BaseConfig):
        key1 = Setting(datacast.enum(EnumTest), required=True)
    return ConfigEnumTest

@pytest.fixture
def ConfigStrEnumTest():
    class ConfigStrEnumTest(BaseConfig):
        key1 = Setting(datacast.enum(StrEnumTest), required=True)
    return ConfigStrEnumTest

def test_int_enum_1(ConfigEnumTest):
    raw_config = {"key1":1}
    cfg = ConfigEnumTest(raw_config)
    assert cfg["key1"] == EnumTest.a

def test_int_enum_2(ConfigEnumTest):
    raw_config = {"key1":2}
    cfg = ConfigEnumTest(raw_config)
    assert cfg["key1"] == EnumTest.b

def test_str_enum_1(ConfigStrEnumTest):
    raw_config = {"key1":"a"}
    cfg = ConfigStrEnumTest(raw_config)
    assert cfg["key1"] == StrEnumTest.a

def test_str_enum_1(ConfigStrEnumTest):
    raw_config = {"key1":"b"}
    cfg = ConfigStrEnumTest(raw_config)
    assert cfg["key1"] == StrEnumTest.b

def test_enum_config_eq(ConfigEnumTest):
    raw_config = {"key1":1}
    cfg = ConfigEnumTest(raw_config)
    cfg2 = ConfigEnumTest(raw_config)
    assert cfg == cfg2

def test_enum_config_not_eq(ConfigEnumTest):
    raw_config = {"key1":1}
    raw_config2 = {"key1":2}
    cfg = ConfigEnumTest(raw_config)
    cfg2 = ConfigEnumTest(raw_config2)
    assert not cfg == cfg2