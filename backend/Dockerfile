##############################################
# 基于python:3.9.16-slim

# 
##############################################
FROM python:3.9.16-slim
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

# 系统环境依赖配置
# 目录设置
WORKDIR /home/ipam_backend
# 更新pip版本
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ uwsgi --upgrade pip


COPY . /home/ipam_backend

# 再次切换工作目录为Django主目录
WORKDIR /home/ipam_backend


# 安装项目所需python第三方库
# 指定setuptools的版本，必须指定，新版本有兼容问题
RUN set -ex \
    && /usr/local/python3/bin/pip3 install setuptools_scm -i https://mirrors.aliyun.com/pypi/simple/ \
    && /usr/local/python3/bin/pip3 install --upgrade pip setuptools==45.2.0 -i https://mirrors.aliyun.com/pypi/simple/ \
    &&/usr/local/python3/bin/pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm -rf /var/cache/yum/*

RUN set -ex \
 && echo -e "yes" | python3 manage.py collectstatic \
 && echo -e python3 manage.py makemigrations \
 && python3 manage.py migrate  --fake
#EXPOSE 8000
EXPOSE 18005
EXPOSE 35055
CMD ["sh", "start.sh"]