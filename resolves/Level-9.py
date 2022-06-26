"""
Author: wudinaonao
Date: 2022-06-25 22:06:24
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:15:54
Description: 




"""
import base64
from io import BytesIO

import requests
from lxml import etree
from PIL import Image
from pyzbar.pyzbar import decode
from typing import List, Tuple
from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        xpath = "/html/body/div[1]/div/div[1]/div/span[2]/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("Parsing failed")

        png_string = results[0][2:-1]
        png_bytes = base64.b64decode(png_string)
        png_image = Image.open(BytesIO(png_bytes))
        result = decode(png_image)[0].data.decode("utf-8")
        return result
