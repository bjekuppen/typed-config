import pytest

def test_unpacking(example_config):
    dict(**example_config) == example_config._config