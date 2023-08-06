from typing import Union

import requests
from requests import Response

from data_classes.FileData import FileData
from data_classes.ModpackData import ModpackData
from data_classes.UserData import UserData


class Utils:
    @staticmethod
    def getData(url: str, data: dict) -> Response:
        r = requests.get(url, params=data)
        return r

    @staticmethod
    def removeNullsFromDict(data: dict) -> dict:
        removed = {k: v for k, v in data.items() if v is not None}
        return removed

    @staticmethod
    def dictToClass(data: dict, obj: Union[type(ModpackData), type(FileData), type(UserData)]) -> Union[ModpackData, FileData, UserData]:
        cls: Union[ModpackData, FileData, UserData] = obj()
        for k, v in data.items():
            cls.__setattr__(k, v)
        return cls
