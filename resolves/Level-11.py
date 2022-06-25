"""
Author: wudinaonao
Date: 2022-06-25 22:30:55
LastEditors: wudinaonao
LastEditTime: 2022-06-25 22:50:43
Description: 




"""
import js2py
import requests
from lxml import etree

from ._Interface import IResolve


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def crack(self, response: requests.Response) -> str:
        xpath = "/html/body/div[1]/div/div[1]/div/script/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("Parse Failed.")

        # ts
        ts_xpath = '//*[@id="pwd"]/@data-ts'
        ts = html.xpath(ts_xpath)[0].strip()

        # stmnt
        url = "https://www.odoo.com/odoo_challenge/static/src/js/challenge.js"
        resp = self._session.get(url)
        getBiskuit = js2py.eval_js(resp.text)
        stmnt = getBiskuit("X-Odoo")
