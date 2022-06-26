"""
Author: wudinaonao
Date: 2022-06-25 22:30:55
LastEditors: wudinaonao
LastEditTime: 2022-06-26 11:47:11
Description: 

      $( document ).ready(function() {
        $("#submit").on('click', function(e) {
          e.preventDefault();
          if (window.location.search.indexOf('challenge')!=-1) {debugger;}
          pwd = $("#pwd").val();
          ts = $("#pwd").data('ts')+'';
          stmnt = getBiskuit('X-Odoo');
          multi = true;
          $(ts.substr(0,5).split('')).each(function( i , j) {
            multi *= stmnt[parseInt(j) +1].charCodeAt(0);
          });

          multi = 1
          for i, j in enumrate(list(ts[0:5])):
            multi *= ord(stmnt[int(j) + 1])

          if (parseInt(pwd.slice(-(--([,,,undefined].join()).length))[0]) * parseInt(pwd.slice(0 - - - 1 - - - - - 1 - - - - 0)[1]) * stmnt.split("All").length == ts.slice(eval(""+''+""+ƒ(1<0)+""+"-"+''+""+ƒ(0<1)+"-"+ƒ(1>0)))) {
            $.ajax("./70/"+ pwd, {
              success: function (o) {
                0===pwd.lastIndexOf(multi.toString().substr(1,4)+stmnt.substring(2,6),0)&&(
                  $.post('submit', {pwd: o, csrf_token:'8a4c3116351c665d6009c3c0b3c81a68829dcd07o1687746953'}).always(function(){window.location.href='/jobs/challenge/next'})
                );
                },
                error: function (o) {
                  console.error('To be or not to be... ');
              }
            });
          }
        });
      });


"""

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
        # url = "https://www.odoo.com/odoo_challenge/static/src/js/challenge.js"
        # resp = self._session.get(url)
        # js = 'function getBiskuit(a){for(var b=a+"=",c=document.cookie.split(";"),d=0;d<c.length;d++){var e=c[d].trim();if(0==e.indexOf(b))return e.substring(b.length,e.length)}return""}'
        # getBiskuit = js2py.eval_js(js)
        # stmnt = getBiskuit("X-Odoo")
        stmnt = "\"!Odoo - All your applications in one single solution\""

        # multi
        multi = 1
        for i, j in enumerate(list(ts[0:5])):
            multi *= ord(stmnt[int(j) + 1])

        answer = str(multi)[1:5] + str(stmnt)[2:6]
        answers = [f"{answer}57", f"{answer}75"]

        url = f"https://www.odoo.com/jobs/challenge/70/{answers[0]}"
        resp = self._session.get(url)
        return resp.text
