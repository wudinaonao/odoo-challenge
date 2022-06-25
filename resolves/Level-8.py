"""
Author: wudinaonao
Date: 2022-06-25 21:56:28
LastEditors: wudinaonao
LastEditTime: 2022-06-25 22:06:15
Description: 




"""
import requests
from lxml import etree

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        url = "https://www.odoo.com/jobs/challenge/challenge"
        resp = self._session.get(url)
        xpath = "//text()"
        html = etree.HTML(resp.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("解析失败")
        answer = "".join(list(filter(lambda x: "#" not in x, results))).strip()
        answer = answer.replace("Password:'", "")
        answer = answer.replace("'", "")
        return answer
