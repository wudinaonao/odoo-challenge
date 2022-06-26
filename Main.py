"""
Author: wudinaonao
Date: 2022-06-25 14:20:40
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:53:14
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
            raise ValueError(f"Not found {name} parser")
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
            raise ValueError("Parsing csrf_token failed")
        return results[0]

    def _check_level(self, response: requests.Response) -> int:
        """解析用户当前进度, 返回一个整数
        Odoo Challenge 目前一共有 11 个级别
        注意, 当未登录时会检测到 Level # / 11"""

        xpath = "/html/body/div[1]/div/div/div/span/h4/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("Parsing progress failed")

        # Example -> Level # / 11
        level = results[0].split(" ")[1]
        if level == "#":
            raise ValueError(f"Please first login, current level is {results[0]}")
        return int(level)

    def _is_finished(self, response: requests.Response) -> bool:
        """check if is finished, 11 questions in total"""
        xpath = "/html/body/div[2]/a/text()"
        html = etree.HTML(response.text, etree.HTMLParser())
        results = html.xpath(xpath)
        if not results:
            raise ValueError("Parsing progress failed")
        results = list(filter(lambda x: str.isdigit(x.strip()), results))
        return len(results) == 11

    def _get_next(self) -> requests.Response:
        """"""
        resp = self._session.get(url=URL)
        if resp.status_code != 200:
            raise ValueError(f"HTTP request failed, code: {resp.status_code}")
        return resp

    def _submit(self, answer: str, csrf_token: str) -> bool:
        url = "https://www.odoo.com/jobs/challenge/submit"
        data = {"csrf_token": csrf_token, "pwd": answer, "signup": ""}
        resp = self._session.post(url, data=data)
        return "wrong=oups" not in resp.url

    def start(self):
        """start challenge"""

        print(f">>> Starting ...")
        
        self._login()

        # check progress
        resp = self._get_next()
        csrf_token = self._parse_csrf_token(resp)
        if self._is_finished(resp):
            print(f">>> Congratulations, it's done")
            return
        level = self._check_level(resp)

        # start
        for currrent_level in range(level, 11 + 1):
            print(f">>> Current level: {currrent_level}")
            resp = self._get_next()
            csrf_token = self._parse_csrf_token(resp)
            parser = self._get_parser(currrent_level)
            answers = parser(self._session).crack(resp)
            is_pass = self._submit(answers, csrf_token)
            if not is_pass:
                raise ValueError(f"Trying parsing failed. answer: {answers}")
            print(f">>> Answer: {answers}")

        print(f">>> Congratulations, it's done")


if __name__ == "__main__":

    email = input(">>> Please input your Email ...\n")
    if not email:
        raise ValueError("Please input correct email")
    odoo = OdooChallenge(email)
    odoo.start()
