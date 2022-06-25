"""
Author: wudinaonao
Date: 2022-06-25 19:50:16
LastEditors: wudinaonao
LastEditTime: 2022-06-25 19:54:24
Description: 




"""
import base64

import requests

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        url = "https://www.odoo.com/jobs/challenge/challenge.css"
        resp = self._session.get(url)
        answer = resp.cookies.get("passwd")
        return answer
