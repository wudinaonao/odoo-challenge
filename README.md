# Odoo Challenge

Odoo Challenge one-click solution

## Originated

Odoo is a fun challenge, originated from an interview question, the intervieewr sent a link to test the level.

all rigth, accept the challenge.

Challenge Url  

> https://www.odoo.com/jobs/challenge

My blog records all my problem solving ideas.

> https://blog.wudinaonao.com/2022/06/23/Odoo-Challenge/

## Why have this script?

Because i'm a Pythoner! 

**Slogan !**

**ANYTHING THAT CAN BE AUTOMATED SHOULD BE AUTOMATED !**

## How to Using

First install package
```
pip install -r requirements.txt
```

Start
```
python Main.py
```

then, input your email, like this

```
>>> Please input your Email ...
hello_john@gmail.com 
```

OK, click enter!

```
>>> Please input your Email ...
hello_john@gmail.com 
>>> Starting ...
>>> Current level: 1
>>> Answer: 929d0e78a50a60b1859cc1761fcad2fe6257e0f5
>>> Current level: 2
>>> Answer: 58e8b561325600f8c2f638a2a8a1a30491f3a0e7
>>> Current level: 3
>>> Answer: Grow your business with Odoo and more than 525549 apps
>>> Current level: 4
>>> Answer: 8cd7ada42d6df7d2c65d723793476c822a908069
>>> Current level: 5
>>> Answer: Odoo-100491021015455100
>>> Current level: 6
>>> Answer: FFC4A513375FDB60a870
>>> Current level: 7
>>> Answer: 932a339ba3c8629a3018ca6bca27274f7e26b6e6
>>> Current level: 8
>>> Answer: fd47426b20af6b52feecd146ee6474a29d50ae6d
>>> Current level: 9
>>> Answer: 2292d3e52f82823abfd438bc30797ee0005bf502
>>> Current level: 10
>>> Answer: 89d072dbe66fb5c48712345f61fbc621260d26fb
>>> Current level: 11
>>> Answer: b5697fa0bfae4b8e122f179878904af2091d8a93
>>> Congratulations, it's done
```

![](https://chevereto.wudinaonao.com/images/2022/06/26/image86163c77feaf84c3.png)

Nice !

## Docker

I built a SPA based on Flask, Vue 3

![](https://chevereto.wudinaonao.com/images/2022/06/27/image.png)

Now, you can build the docker image

```
docker build --build-arg BUILD_DATE="$(date "+%F %T")"  --tag wudinaonao/flask-odoo-challenge:latest .
```

Run container
```
docker-compose up -d
```

OK, now we can open browser, input url `http://127.0.0.0:8854`

very nice!

input a email, then click button

waiting...

![](https://chevereto.wudinaonao.com/images/2022/06/27/image66bfc8dc1e7c44c7.png)

good !

Maybe you can use the website I have built ...

> https://odoo.wudinaonao.com