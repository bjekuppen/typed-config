from typing import Callable, Any

class Setting():
    def __init__(self, datacast:Callable[[Any], Any]=str, required:bool=False): #type: ignore[assignment] #mypy doesn't like the str as default value, possible fix? 
        self.datacast = datacast
        self.required = required