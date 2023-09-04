# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      routes
   Description:
   Author:          Lijiamin
   date：           2023/4/4 20:39
-------------------------------------------------
   Change Activity:
                    2023/4/4 20:39
-------------------------------------------------
"""
from open_ipam.tasks import ip_am_update_main

routes = {
    "ipaddr_update": ip_am_update_main,
}