from typing import Callable, Any, TypeVar, Union

BaseConfig = TypeVar("BaseConfig")


class Setting():
    def __init__(self, datacast:Callable[[Any], Any]=str, required:bool=False): 
        self.datacast = datacast
        self.required = required

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(datacast={self.datacast}, required={self.required})"

class SettingGroup():
    def __init__(self, config:BaseConfig, required:bool=False): 
        self.config = config
        self.required = required

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(config={self.config}, required={self.required})"
    
class SettingList():
    def __init__(self, setting:Union[Setting, SettingGroup]): 
        self.setting = setting

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(setting={self.setting})"