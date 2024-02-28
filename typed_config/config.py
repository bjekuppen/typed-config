from typing import Any, Type
from .exceptions import RequiredError, UndefinedKeyError
from .setting import Setting, SettingGroup, SettingList

import json
import yaml #type: ignore[import-untyped]

class BaseConfig():
    
    def __init__(self, config:dict[str, Any]) -> None:
        self._raw_config = config
        self.__check_undefined_keys()
        self.__load_config()

    @classmethod
    def load_json(cls, file_path:str) -> Type["BaseConfig"]:
        with open(file_path, 'r') as f:
            raw_config = json.load(f)
        return cls(raw_config) #type: ignore[return-value]

    @classmethod
    def load_yaml(cls, file_path:str)  -> Type["BaseConfig"]:
        with open(file_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        return cls(raw_config) #type: ignore[return-value]

    def __check_undefined_keys(self) -> bool:
        config_keys = self.__get_config_keys()
        for key in self._raw_config.keys():
            if key in config_keys:
                pass
            else:
                raise UndefinedKeyError(f"{key} is invalid.")
        return True

    def __load_config(self) -> None:
        self._config: dict[str, Any] = {}

        class_variables = self.__get_config_keys()
        for variable_name, value in class_variables.items():
            try:
                user_input = self._raw_config[variable_name]
            except KeyError:
                if type(value) == SettingList:
                    if value.setting.required:
                        raise RequiredError()
                    else:
                        continue
                if value.required:
                    raise RequiredError()
                else:
                    continue
            if type(value) == Setting:
                self._config[variable_name] = value.datacast(user_input)
            if type(value) == SettingGroup:
                self._config[variable_name] = value.config(user_input) #type: ignore[operator]
            if type(value) == SettingList:
                self._config[variable_name] = []
                for item in user_input:
                    if type(value.setting) == Setting:
                        self._config[variable_name].append(value.setting.datacast(item))
                    if type(value.setting) == SettingGroup:
                        self._config[variable_name].append(value.setting.config(item)) #type: ignore[operator]

    def __get_config_keys(self) -> dict[str, Any]:
        def filter_items(key:str, value:Any) -> bool:
            return isinstance(value, (Setting, SettingGroup, SettingList))
        return {key: value for key, value in vars(type(self)).items() if filter_items(key, value)}


    def __getitem__(self, key:str) -> Any:
        if type(key) != str:
            raise TypeError("Only str supported")
        return self._config[key]
    
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(config={self._raw_config})"
    
    def __getattribute__(self, name):
        if name != '_config':
            try:
                value = self._config[name]
            except (KeyError, AttributeError):
                return object.__getattribute__(self, name)
            else:
                return value
        else:
            return object.__getattribute__(self, name)

    def __eq__(self, other: Type["BaseConfig"]) -> bool: #type: ignore[override]
        return self._config == other._config
