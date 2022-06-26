"""
Author: wudinaonao
Date: 2022-06-25 14:22:35
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:14:48
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
        url = "https://www.odoo.com/jobs/challenge/challenge.css"
        resp = self._session.get(url)
        atob = resp.text.split(",")[1].strip()
        atob = atob.replace("atob('", "")
        atob = atob.replace("')", "")
        pwd = base64.b64decode(atob).decode("utf-8")
        return pwd
