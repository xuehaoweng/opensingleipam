##############################################
# 基于python:3.9.16-slim

# 
##############################################
FROM python:3.9.16-slim
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

# 系统环境依赖配置
# 目录设置
WORKDIR /home/ipam_backend
# 从gitlab仓库拉取
RUN set -ex \
    # 预安装所需组件
    && yum install -y python-pip \
    && yum install -y python-devel \
    && yum install -y openldap-devel \
    && yum install -y python36-devel \
# 基础环境配置
RUN set -ex \
    # 修改系统时区为东八区
    && rm -rf /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum install -y vim \
    # 安装定时任务组件
    && yum -y install cronie\
    && mkdir -p /home/ipam_backend
# 支持中文
RUN yum install kde-l10n-Chinese -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 更新pip版本
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ uwsgi --upgrade pip
ENV LC_ALL zh_CN.UTF-8


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