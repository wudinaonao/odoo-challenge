"""
Author: wudinaonao
Date: 2022-06-25 14:22:18
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:53:43
Description: 




"""
from abc import ABCMeta, abstractmethod
from typing import List, Tuple

import requests


class IResolve(metaclass=ABCMeta):
    """解析类接口, 每个解析类都需要实现该接口"""

    @abstractmethod
    def __init__(self, session: requests.Session) -> None:
        self._session = session

    @abstractmethod
    def crack(self, response: requests.Response) -> str:
        ...

