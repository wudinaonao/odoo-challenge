"""
Author: wudinaonao
Date: 2022-06-25 14:22:18
LastEditors: wudinaonao
LastEditTime: 2022-06-25 19:39:18
Description: 




"""
from abc import ABCMeta, abstractmethod

import requests


class IResolve(metaclass=ABCMeta):
    """解析类接口, 每个解析类都需要实现该接口"""

    @abstractmethod
    def __init__(self, session: requests.Session) -> None:
        self._session = session

    @abstractmethod
    def crack(self, response: requests.Response) -> str:
        ...

    def submit(self, answer: str, csrf_token: str) -> bool:
        url = "https://www.odoo.com/jobs/challenge/submit"
        data = {"csrf_token": csrf_token, "pwd": answer, "signup": ""}
        resp = self._session.post(url, data=data)
        
