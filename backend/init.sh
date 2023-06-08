#!/bin/bash
python3 manage.py makemigrations users
python3 manage.py migrate users
python3 manage.py makemigrations
python3 manage.py migrate

# 做静态文件收集
echo -e "yes" | python3 manage.py collectstatic
echo "init success!"
echo "starting web server!"
sh start.sh web