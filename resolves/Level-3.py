"""
Author: wudinaonao
Date: 2022-06-25 19:45:17
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:16:23
Description: 




"""
import base64
from typing import List, Tuple

import requests

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        answer =  response.headers.get(
            "it-is-the-long-secret-that-you-are-looking-for")
        if not answer:
            raise ValueError("Parsing failed")
        return answer
