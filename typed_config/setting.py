from typing import Callable, Any, TypeVar, Union

BaseConfig = TypeVar("BaseConfig")


class Setting():
    def __init__(self, datacast:Callable[[Any], Any]=str, required:bool=False): 
        self.datacast = datacast
        self.required = required

class SettingGroup():
    def __init__(self, config:BaseConfig, required:bool=False): 
        self.config = config
        self.required = required
    
class SettingList():
    def __init__(self, setting:Union[Setting, SettingGroup]): 
        self.setting = setting