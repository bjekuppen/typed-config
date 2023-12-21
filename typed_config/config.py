from typing import Any
from .exceptions import RequiredError
from .setting import Setting


class BaseConfig():
    
    def __init__(self, config:dict[str, Any]) -> None:
        self.raw_config = config
        self.__load_config()

    def __load_config(self) -> None:
        self._config: dict[str, Any] = {}

        class_variables = self.__get_class_variables()
        for variable_name, value in class_variables.items():
            if type(value) == Setting:
                try:
                    user_input = self.raw_config[variable_name]
                except KeyError:
                    if value.required:
                        raise RequiredError()
                    else:
                        continue
                self._config[variable_name] = value.datacast(user_input)

    def __get_class_variables(self) -> dict[str, Any]:
        return {key: value for key, value in vars(type(self)).items() if not (key.startswith('__') and key.endswith('__'))}

    def __getitem__(self, key:str) -> Any:
        if type(key) != str:
            raise TypeError("Only str supported")
        return self._config[key]