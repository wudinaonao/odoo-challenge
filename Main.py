"""
Author: wudinaonao
Date: 2022-06-25 14:20:40
LastEditors: wudinaonao
LastEditTime: 2022-06-25 20:07:38
Description: 




"""
import requests
from lxml import etree

import resolves
from resolves._Interface import IResolve

URL = "https://www.odoo.com/jobs/challenge/next"


class OdooChallenge(object):
    """Odoo 挑战赛一键通关"""

    def __init__(self, email: str) -> None:
        self._email = email
        self._session = requests.Session()

        # 加载解析器
        # self._parsers = {}
        # self._load_parser()

    # def _load_parser(self):
    #     ...

    def _get_parser(self, level: int) -> IResolve:
        """获取对应题目的解析器"""
        name = f"Level-{level}"
        if name not in resolves.__modules_class__:
            raise ValueError(f"没有找到 {name} 的解析器")
        return resolves.__modules_class__[name].Resolve

    def _login(self):
        """登录"""

        # First
        resp = self._get_next()
        csrf_token = self._parse_csrf_token(resp)

        # Login
        login_url = "https://www.odoo.com/jobs/challenge/login"
        data = {
            "csrf_token": csrf_token,
            "login": self._email,
            "signup": "",
        }
        self._session.post(url=login_url, data=data)

    def _parse_csrf_token(self, response: requests.Response) -> str:
        """解析 csrf_token"""
        xpath = "/html/body/div[1]/div/div/div/form/input/@value"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("解析 csrf_token 失败")
        return results[0]

    def _check_level(self, response: requests.Response) -> int:
        """解析用户当前进度, 返回一个整数
        Odoo Challenge 目前一共有 11 个级别
        注意, 当未登录时会检测到 Level # / 11"""

        xpath = "/html/body/div[1]/div/div/div/span/h4/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("解析进度失败")

        # Example -> Level # / 11
        level = results[0].split(" ")[1]
        if level == "#":
            raise ValueError(f"请先登录, 解析进度为 {results[0]}")
        return int(level)

    def _get_next(self) -> requests.Response:
        """"""
        resp = self._session.get(url=URL)
        if resp.status_code != 200:
            raise ValueError(f"HTTP 请求失败, 响应码: {resp.status_code}")
        return resp

    def _submit(self, answer: str, csrf_token: str) -> bool:
        url = "https://www.odoo.com/jobs/challenge/submit"
        data = {"csrf_token": csrf_token, "pwd": answer, "signup": ""}
        resp = self._session.post(url, data=data)
        return "wrong=oups" not in resp.url

    def start(self):
        # 
        self._login()

        # 
        resp = self._get_next()
        csrf_token = self._parse_csrf_token(resp)

        # 
        level = self._check_level(resp)

        #
        for currrent_level in range(level, 11 + 1):

            print(f">>> 当前 Level: {currrent_level}")

            resp = self._get_next()
            csrf_token = self._parse_csrf_token(resp)
            parser = self._get_parser(currrent_level)
            answer = parser(self._session).crack(resp)
            is_pass = self._submit(answer, csrf_token)
            if not is_pass:
                raise ValueError(f"尝试解析失败. answer: {answer}")

            print(f">>> 答案: {answer}")

if __name__ == "__main__":

    # email = input(">>> Please input your Email ...\n")
    email = "nao@nao.com"
    
    if not email:
        raise ValueError("请输入一个正确的 Email")
    odoo = OdooChallenge(email)
    odoo.start()
