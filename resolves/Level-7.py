"""
Author: wudinaonao
Date: 2022-06-25 20:09:32
LastEditors: wudinaonao
LastEditTime: 2022-06-25 21:34:32
Description: 




"""
import base64
import decimal
import json
import math
import time

import requests

from ._Interface import IResolve


class CalculatePi(object):
    """Chudnovsky"""

    @classmethod
    def calc(cls, index: int) -> int:
        """calculate pi index numbers"""
        decimal.getcontext().prec = index

        root = decimal.Decimal(100.024996876)
        oldroot = decimal.Decimal(0)

        while root != oldroot:

            oldroot = root

            root = decimal.Decimal(
                decimal.Decimal(0.5) *
                decimal.Decimal(root + decimal.Decimal(10005 / root)))

        C = decimal.Decimal(426880 * root)

        L = decimal.Decimal(13591409)
        X = decimal.Decimal(1)
        M = decimal.Decimal(1)

        u = decimal.Decimal(decimal.Decimal(M * L) / X)
        oldu = decimal.Decimal(3)

        pi = decimal.Decimal(3)

        q = int(0)

        while u != oldu:

            oldu = u

            L = decimal.Decimal(L + 545140134)
            X = decimal.Decimal(-262537412640768000 * X)
            M = decimal.Decimal(M * decimal.Decimal(
                decimal.Decimal((12 * q + 2) * (12 * q + 6) *
                                (12 * q + 10)) / decimal.Decimal((q + 1)**3)))

            u += decimal.Decimal(decimal.Decimal(M * L) / X)

            q += 1

        pi = decimal.Decimal(C / u)

        return int(str(pi)[-4])


class Resolve(IResolve):

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session)
        self._session = session

    def _merge_url(self, response: requests.Response) -> str:
        # 查找 URL 片段
        part1 = response.headers.get("it-is-the-part-1-of-url")
        url = "https://www.odoo.com/jobs/challenge/challenge.css"
        resp = self._session.get(url)
        part2 = resp.cookies.get("It-Is-The-Part-2-Of-Url")

        # 1 -> /jobs/challenge/da4/<part2>/prime.json
        # 2 -> /jobs/challenge/<part1>/b95/prime.json

        part1 = part1.replace("<part2>", "")\
            .split("/")
        part2 = part2.replace("<part1>", "")\
            .replace("\"", "")\
            .split("/")

        complete = []
        for i in range(len(part1)):
            if part1[i]:
                complete.append(part1[i])
            else:
                complete.append(part2[i])
        url = "/".join(complete)
        return url

    def _get_pi(self, instructions: str) -> int:
        index = int("".join(list(filter(str.isdigit, instructions))))
        return CalculatePi.calc(index + 4)

    def _is_prime(self, x: int) -> bool:
        """check if is prime
        referencen link https://zhuanlan.zhihu.com/p/107300262"""
        if x == 2 or x == 3:
            return True
        if x % 6 != 1 and x % 6 != 5:
            return False
        for i in range(5, int(x**0.5) + 1, 6):
            if x % i == 0 or x % (i + 2) == 0:
                return False
        return True

    def crack(self, response: requests.Response) -> str:
        url = self._merge_url(response)
        url = f"https://www.odoo.com{url}"
        resp = self._session.get(url)
        resp = json.loads(resp.text)

        # get right shift length
        instructions = resp["instructions"]
        right_n = self._get_pi(instructions)

        # filter not prime numbers
        numbers = resp["numbers"]
        numbers = list(filter(lambda x: self._is_prime(x), numbers))

        #
        answer = "".join(list(map(lambda x: chr(x >> right_n), numbers)))
        return answer
