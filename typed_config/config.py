from typing import Any, Type
from .exceptions import RequiredError
from .setting import Setting, SettingGroup, SettingList

import json
import yaml #type: ignore[import-untyped]

class BaseConfig():
    
    def __init__(self, config:dict[str, Any]) -> None:
        self.raw_config = config
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

    def __load_config(self) -> None:
        self._config: dict[str, Any] = {}

        class_variables = self.__get_class_variables()
        for variable_name, value in class_variables.items():
            try:
                user_input = self.raw_config[variable_name]
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

    def __get_class_variables(self) -> dict[str, Any]:
        def filter_items(key:str, value:Any) -> bool:
            return isinstance(value, (Setting, SettingGroup, SettingList))
        return {key: value for key, value in vars(type(self)).items() if filter_items(key, value)}


    def __getitem__(self, key:str) -> Any:
        if type(key) != str:
            raise TypeError("Only str supported")
        return self._config[key]
    
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(config={self.raw_config})"