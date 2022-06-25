"""
Author: wudinaonao
Date: 2022-06-25 22:20:03
LastEditors: wudinaonao
LastEditTime: 2022-06-25 22:29:45
Description: 




"""
import base64
from io import BytesIO

import requests
from lxml import etree
from PIL import Image
from pyzbar.pyzbar import decode

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

        self._pwd = ["" for _ in range(40)]

    def decrypt(self, text, fr, to, by):
        for i, j in enumerate(range(fr, to, by)):
            self._pwd[j] = text[i]


    def crack(self, response: requests.Response) -> str:
        xpath = "/html/body/div[1]/div/div[1]/div/pre[2]/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("解析失败")

        output = results[0].strip()
        output = output.split("\n")

        for i in range(0, len(output), 2):
            row = output[i].replace(">>> print(r(pwd,", "").replace("))", "").strip()
            rows = row.split(",")
            rows = list(map(lambda x: x.strip(), rows))
            self.decrypt(output[i + 1], int(rows[0]), int(rows[1]), int(rows[2]))

        answer = "".join(self._pwd)
        return answer
