# -*- coding: utf-8 -*-

import logging
from confload.confload import config

logger = logging.getLogger('nacos')


def nacos_init():
    if not config.local_dev:
        metadata = {
            'queue': config.queue,
            'routing_key': config.routing_key,
            # 'menu': config.default_menu,
        }
        config.registerService(serviceIp=config.backend_ip,
                               servicePort=config.backend_port,
                               serviceName=config.queue, groupName="default",
                               metadata=metadata)
        config.healthyCheck()


