FROM python:3.8.13-slim-buster

# 工作目录
WORKDIR /usr/app

# 拷贝文件
COPY . .

# 设置环境变量
ARG BUILD_DATE
ENV BUILD_DATE=$BUILD_DATE

# 安装 MySQL 驱动 OpenCV 依赖
RUN echo "" > /etc/apt/sources.list \
    && echo "deb http://mirrors.cloud.tencent.com/debian/ buster main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.cloud.tencent.com/debian-security buster/updates main" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.cloud.tencent.com/debian/ buster-updates main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.cloud.tencent.com/debian/ buster-backports main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.cloud.tencent.com/debian-security buster/updates main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.cloud.tencent.com/debian/ buster main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.cloud.tencent.com/debian/ buster-updates main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.cloud.tencent.com/debian/ buster-backports main non-free contrib" >> /etc/apt/sources.list \
    && apt update \
    && apt install python3-opencv -y \
    && apt install default-libmysqlclient-dev gcc -y \
    && mkdir log

# 安装依赖
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple \
    && pip install --no-cache-dir -r requirements.txt \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone

# 入口点
ENTRYPOINT ["python", "/usr/app/App.py"]

# Dockerfile 详细说明 
# https://www.runoob.com/docker/docker-dockerfile.html
