import pytest

def test_test(example_config):
    assert example_config.key1.key1[0].key1 == ["1", "2"]
    assert example_config.key1.key1[0].key2 == ["3", "4"]
    assert example_config.key1.key1[0].key3 == "5"
    assert example_config.key1.key1[1].key1 == ["6", "7"]
    assert example_config.key1.key1[1].key2 == ["8", "9"]
    assert example_config.key1.key1[1].key3 == "10"

    assert example_config.key1.key2[0].key1 == ["11", "12"]
    assert example_config.key1.key2[0].key2 == ["13", "14"]
    assert example_config.key1.key2[0].key3 == "15"
    assert example_config.key1.key2[1].key1 == ["16", "17"]
    assert example_config.key1.key2[1].key2 == ["18", "19"]
    assert example_config.key1.key2[1].key3 == "20"

    assert example_config.key1.key3 == "21"

    assert example_config.key2 == "22"