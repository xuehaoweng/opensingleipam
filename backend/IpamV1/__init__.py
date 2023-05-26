import sys

import pymysql

from IpamV1 import settings
# from utils.nacos import nacos
# from utils.nacos import nacos
from utils.nacos_register import nacos_init
from .celery import app as celery_app

pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

__all__ = ['celery_app']
nacos_init()
# 如果你需要注册nacos，请打开以下注释

# if sys.argv[1] not in ["makemigrations", "migrate", "collectstatic", "runserver", "createsuperuser"]:
#     # 注册服务
#     nacosServer = nacos(ip=settings.NACOSIP, port=settings.NACOSPORT)
#     nacosServer.registerService(serviceIp=settings.SERVERIP, servicePort=settings.SERVERPORT, serviceName="ipam",
#                                 groupName="default")
#     nacosServer.healthyCheck()
