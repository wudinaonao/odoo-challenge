"""
Author: wudinaonao
Date: 2022-06-25 19:57:48
LastEditors: wudinaonao
LastEditTime: 2022-06-25 20:05:26
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
        xpath = "/html/body/div[1]/div/div[1]/div/pre/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("解析失败")
        code = results[0]

        # 查找密文
        rows = list(filter(lambda row: "if(tmp == " in row, code.split("\n")))
        tmp = rows[0]
        tmp = tmp.replace("if(tmp == \"", "")
        tmp = tmp.replace("\")", "")
        tmp = tmp.strip()
        tmp = tmp.split(" ")
        
        # 解析
        idx = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pwd = "".join([idx[int(index)] for index in tmp])
        return pwd
