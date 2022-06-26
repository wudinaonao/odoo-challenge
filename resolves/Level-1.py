"""
Author: wudinaonao
Date: 2022-06-25 14:22:28
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:42:13
Description: 




"""
from typing import List, Tuple

import requests
from lxml import etree

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        xpath = "/html/body/div[1]/div/div[1]/div/form/div[1]/div/input[1]/@value"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("Parsing failed")
        return results[0]
