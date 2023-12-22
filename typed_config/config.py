from typing import Any
from .exceptions import RequiredError
from .setting import Setting, SettingGroup, SettingList


class BaseConfig():
    
    def __init__(self, config:dict[str, Any]) -> None:
        self.raw_config = config
        self.__load_config()

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
        return {key: value for key, value in vars(type(self)).items() if not (key.startswith('__') and key.endswith('__'))}


    def __getitem__(self, key:str) -> Any:
        if type(key) != str:
            raise TypeError("Only str supported")
        return self._config[key]