#!/bin/bash
import os
python3 manage.py makemigrations
python3 manage.py migrate

# 做静态文件收集
echo -e "yes" | python3 manage.py collectstatic

#sh start.sh web