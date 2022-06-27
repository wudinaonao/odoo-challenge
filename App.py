"""
Author: wudinaonao
Date: 2022-06-27 01:56:13
LastEditors: wudinaonao
LastEditTime: 2022-06-27 15:29:14
Description: 




"""
from gevent import monkey

monkey.patch_all()

import mimetypes
import multiprocessing
import os
import threading
import time
from typing import Dict, Tuple

import gunicorn.app.base
import requests
from flask import Flask, jsonify, render_template, request
from lxml import etree

import resolves
from resolves._Interface import IResolve

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('image/x-icon', '.ico')

app = Flask(__name__,
            template_folder="template",
            static_url_path='',
            static_folder="template")

# task save time 8 hour
TASK_CACHE_TIME = 3600 * 8


class GunicornBootstrap(gunicorn.app.base.BaseApplication):
    """自定义 Gunicorn 启动器"""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Solve(object):
    """Solve for save request status

        email:      Email
        status:     WAIT
                    RUNNING
                    FINISHED
                    ERROR
        join_time:  task join time, unit second
        stdout:     task running output information

    """
    URL = "https://www.odoo.com/jobs/challenge/next"

    def __init__(self, email: str) -> None:
        self.email = email
        self.join_time = int(time.time())
        self.status = "WAIT"
        self.stdout = ""
        self._session = requests.Session()

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
            "login": self.email,
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
            raise ValueError(
                f"Please first login, current level is {results[0]}")
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
        resp = self._session.get(url=self.URL)
        if resp.status_code != 200:
            raise ValueError(f"HTTP request failed, code: {resp.status_code}")
        return resp

    def _submit(self, answer: str, csrf_token: str) -> bool:
        url = "https://www.odoo.com/jobs/challenge/submit"
        data = {"csrf_token": csrf_token, "pwd": answer, "signup": ""}
        resp = self._session.post(url, data=data)
        return "wrong=oups" not in resp.url

    def _run(self):
        """start challenge"""

        self._log(f">>> Starting ...")
        self.status = "RUNNING"

        self._log(f">>> Login {self.email} ...")
        self._login()

        # check progress
        resp = self._get_next()
        csrf_token = self._parse_csrf_token(resp)
        if self._is_finished(resp):
            self._log(f">>> Congratulations, it's done")
            self.status = "FINISHED"
            return
        level = self._check_level(resp)

        # start
        for currrent_level in range(level, 11 + 1):
            self._log(f">>> Current level: {currrent_level}")
            resp = self._get_next()
            csrf_token = self._parse_csrf_token(resp)
            parser = self._get_parser(currrent_level)
            answers = parser(self._session).crack(resp)
            is_pass = self._submit(answers, csrf_token)
            if not is_pass:
                raise ValueError(f"Trying parsing failed. answer: {answers}")
            self._log(f">>> Answer: {answers}")

        self._log(f">>> Congratulations, it's done")
        self.status = "FINISHED"

    def start(self):
        try:
            self._run()
        except Exception as e:
            self.status = "ERROR"
            self._log(str(e))

    def _log(self, string: str):
        self.stdout += f"{string}\n"


class Scheduler(object):
    """"""

    def __init__(self) -> None:
        self._tasks: Dict[str, Solve] = {}
        self._lock = threading.Lock()

        clear_expired = threading.Thread(target=self._clear_expired)
        clear_expired.name = "Clear expired task"
        clear_expired.start()

    def get(self, email: str) -> Tuple[Solve, None]:
        if email in self._tasks:
            return self._tasks[email]
        return None

    def exist(self, email: str) -> bool:
        return email in self._tasks

    def add(self, email: str):
        solve = Solve(email)
        self._tasks[email] = solve
        task = threading.Thread(target=solve.start)
        task.name = email
        task.start()

    def _clear_expired(self):
        """clear expired task"""
        while True:
            with self._lock:
                c_time = int(time.time())
                for key in list(self._tasks.keys()):
                    join_time = self._tasks[key].join_time
                    is_expired = (c_time - join_time) > TASK_CACHE_TIME
                    finished = self._tasks[key].status in ("FINISHED", "ERROR")
                    if is_expired and finished:
                        self._tasks.pop(key)
            time.sleep(TASK_CACHE_TIME)


scheduler = Scheduler()


@app.route("/api/solve")
def solve():
    email = request.args.get("email")
    if not email:
        return jsonify(status="ERROR", msg="Email is empty")

    if not scheduler.exist(email):
        scheduler.add(email)
    task = scheduler.get(email)
    return jsonify(status=task.status, msg=task.stdout)


@app.route("/api/info")
def info():
    return jsonify(build_date=os.environ("BUILD_DATE"))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':

    # development
    # app.run("0.0.0.0", debug=True)

    # production

    host = "0.0.0.0"
    port = 5000
    options = {
        "bind": f"{str(host)}:{str(port)}",
        "workers": 1,
        "worker_class": "gevent",
    }
    GunicornBootstrap(app, options).run()
