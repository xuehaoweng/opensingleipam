# -*- coding: utf-8 -*-

import json
import os
import django
from django.core.management import BaseCommand

from open_ipam.models import Subnet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IpamV1.settings')
django.setup()
from IpamV1.settings import BASE_DIR
from django.apps import apps


# from apps.asset.models import Idc


def main():
    with open(os.path.join(BASE_DIR, 'utils', 'init_subnet.json'), 'r', encoding="utf-8") as load_f:
        code_list = json.load(load_f)
        for table, values in code_list.items():
            print(table, values)
            my_model = apps.get_model("open_ipam", table)
            if my_model:
                for value in values:
                    # if table == "subnet":
                    #     value['master_subnet'] = Subnet.objects.get(id=value['master_subnet'])
                    my_model.objects.get_or_create(**value)


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init_subnet
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print(f"正在准备初始化Subnet数据...")
        main()
        print("数据初始化Subnet数据完成！")
