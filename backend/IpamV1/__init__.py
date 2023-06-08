# from __future__ import absolute_import, unicode_literals
import logging
import pymysql

logger = logging.getLogger('server')

pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

