FROM ubuntu:20.04
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt update && apt install -y iputils-ping python3 python3-pip python3-tk libffi-dev libssl-dev
RUN pip3 install -i https://pypi.douban.com/simple/ -U pip
RUN pip3 config set global.index-url https://pypi.douban.com/simple/
RUN pip3 install uwsgi==2.0.19.1

ADD [".", "/app"]
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["uwsgi", "--ini", "uwsgi.ini"]