# -*- coding: utf-8 -*-
import asyncio

import pandas as pd
import json
import logging
import os
import pathlib
import time
from datetime import datetime, timedelta, date

from celery import shared_task, current_app

from IpamV1 import settings
from celery_once import QueueOnce
from open_ipam.models import IpAddress, Subnet
from open_ipam.tools.phpipam import PhpIpamApi

from utils.ipam_utils import IpAmForNetwork
from utils.mongo_api import IpamMongoOps
from utils.send_email import send_mail
from IpamV1.settings import BASE_DIR
from netaddr import IPNetwork, IPSet

logger = logging.getLogger('ipam')

# 写入记录日志
def write_log(filename, datas):
    try:
        isExists = os.path.exists(os.path.dirname(filename))
        if not isExists:
            os.makedirs(os.path.dirname(filename))
    except Exception as e:
        pass
    with open(filename, 'a', encoding='utf-8-sig') as f:
        for row in datas:
            f.write(row)
    logger.info('Write Log Done!')

# 获取所有任务task
@shared_task(base=QueueOnce, once={'graceful': True})
def get_tasks():
    celery_app = current_app
    # celery_tasks = [task for task in celery_app.tasks if not task.startswith('celery.')]
    res = list(sorted(name for name in celery_app.tasks
                      if not name.startswith('celery.')))
    return json.dumps({'result': res})


@shared_task(base=QueueOnce, once={'graceful': True})
def ipam_scan():
    pass


# 数据同步-同步原有phpipam的IP地址数据
@shared_task(base=QueueOnce, once={'graceful': True})
def sync_ipam_ipaddress_main():
    task_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('同步PHPIPAM地址记录开始', task_start_time)
    start_time = time.time()
    phpipamapi = PhpIpamApi()
    # 根据subnet下的ip汇总的总地址记录表
    all_subnet_ipaddress = phpipamapi.get_all_addresses_by_subnet()
    all_subnet_ipaddress_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('同步all_subnet_ipaddress_time', all_subnet_ipaddress_time)
    whole_ipaddress = []
    for subnet_address in all_subnet_ipaddress:
        for address_info in subnet_address:
            address_list = subnet_address[address_info]
            whole_ipaddress.extend(address_list)
    whole_ipaddress_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('同步whole_ipaddress_time', whole_ipaddress_time)
    # map形式切换for循环的ip地址新增逻辑
    list(map(create_ip_address, whole_ipaddress))

    end_time = time.time()
    total_time = int(end_time - start_time)
    task_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('花费总时间{}s'.format(total_time))
    logger.info('同步PHPIPAM地址记录结束', task_end_time)

# 新建ip地址实例
def create_ip_address(address):
    try:
        subnet_instance = Subnet.objects.filter(subnet_id=int(address['subnetId'])).first()
        address_kwargs = {
            "subnet": subnet_instance,
            "ip_address": address['ip'],
            "description": address.get('description', 'note'),
            "tag": address['tag'],
            "lastOnlineTime": json.loads(address['note'])['Last Online Time'] if address[
                                                                                     'note'] is not None else
            str(date.today())
        }
        IpAddress.objects.create(**address_kwargs)
    except Exception as e:
        IpamMongoOps.insert_fail_ip(address)
        logger.info('插入地址失败', e, address)


# 数据同步-同步原有phpipam的网段数据
@shared_task(base=QueueOnce, once={'graceful': True})
def sync_ipam_subnet_main():
    task_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('同步PHPIPAM网段记录开始', task_start_time)
    start_time = time.time()
    # Subnet.objects.filter(description__icontains="")
    phpipamapi = PhpIpamApi()
    all_subnets = phpipamapi.get_all_subnets()
    first_level_list = []
    # logger.info(len(all_subnets))
    for subnet in all_subnets:
        if subnet['masterSubnetId'] == '0':
            # logger.info('一级结构')
            first_level_list.append(subnet)
            # 插入一级结构网段
            kwargs = {
                "name": subnet['subnet'] + '/' + subnet['mask'],
                "subnet": "{}/{}".format(IPNetwork(subnet['subnet']).network, subnet['mask']),
                "mask": subnet['mask'],
                "description": subnet.get('description', "空"),
                "subnet_id": subnet.get('id', 0),
            }
            try:
                Subnet.objects.update_or_create(**kwargs)
            except Exception as e:
                logger.info(subnet['subnet'])
                IpamMongoOps.insert_fail_subnet(subnet['subnet'])
                logger.info('插入失败{}'.format(e))
            all_subnets.remove(subnet)

    second_level = []
    # 遍历剩下不等于ROOT的网段

    for second_subnet in all_subnets:
        # 插入非ROOT网段结构
        second_kwargs = {
            "name": second_subnet['subnet'] + '/' + second_subnet['mask'],
            "subnet": "{}/{}".format(IPNetwork(second_subnet['subnet']).network, second_subnet['mask']),
            "mask": second_subnet['mask'],
            "description": second_subnet.get('description', "空"),
            "subnet_id": second_subnet.get('id', 0),
            "master_subnet": Subnet.objects.filter(subnet_id=second_subnet.get('masterSubnetId')).first()
        }
        try:
            Subnet.objects.update_or_create(**second_kwargs)
        except Exception as e:
            logger.info(second_subnet['subnet'])
            IpamMongoOps.insert_fail_subnet(second_subnet['subnet'])
            logger.info('插入失败{}'.format(e))

    end_time = time.time()
    total_time = int(end_time - start_time)
    task_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('花费总时间{}s'.format(total_time))
    logger.info('同步PHPIPAM网段记录结束', task_end_time)


# IPAM地址全网更新子任务
@shared_task(base=QueueOnce, once={'graceful': True})
async def ip_am_update_sub_task(ip):
    ip_address_model = IpAddress
    # 文件名-操作失败的IP地址写入文件中
    file_time = datetime.now().strftime("%Y-%m-%d")
    # netops_ipam_ip_fail文件路径.log
    ip_am_ip_fail_file = os.path.join(BASE_DIR, 'media', 'ipam', "netops_ipam_ip_fail-{}.log".format(file_time))
    # 在ipam地址表取地址实例
    ip_address_instance = ip_address_model.objects.filter(ip_address=ip).values().first()

    tmp_description = {"Last Online Time": file_time, }
    lastOnlineTime = file_time

    # TODO 判断IP地址是否在Netops-IPAM中有记录

    # IP地址暂时不存在Netops-IPAM中 则不存在子网网段IP
    if ip_address_instance is None:
        # 网段不存在,则去判断16位存不存在,看是否需要先新增网段
        # TODO V6地址怎么查询上一级网段-目前策略直接跳过
        subnet16_id = IpAmForNetwork.get_sixteen_subnet_id(ip=ip)
        if subnet16_id:
            subnet24 = IPNetwork(f'{ip}/24').network
            # logger.info(subnet24)
            # 查询是否存在24位网段
            subnet24_instance = Subnet.objects.filter(subnet=str(subnet24) + "/24").first()
            if subnet24_instance:
                subnet_insert_id = subnet24_instance.id
            else:
                # 新建24位网段
                subnet_instance = Subnet(subnet=str(subnet24) + "/24", mask=24, master_subnet_id=subnet16_id,
                                         description=f'netops_ipam {file_time} 新建网段')
                subnet_instance.save()
                subnet_insert_id = subnet_instance.id

            """
            # 新增IP地址信息置位tag=4  未分配已使用
            1、查询除log_time字段外,是否有完全匹配,如果有就只更新log_time字段, 如果log_time字段一致,则不进行任何操作
            2、如果查询不到数据,则新增该字段
            """
            # TODO 到新增地址表
            IpamMongoOps.post_success_ip(ip)
            # 新建该IP地址实例、绑定IP地址插入的归属网段ID
            ip_create_instance = IpAddress(subnet_id=subnet_insert_id, ip_address=ip, tag=4,
                                           description=json.dumps(tmp_description))
            ip_create_instance.save()
        # 若不存在16位网段
        else:
            # 不存在16位网段-直接 TODO 丢弃到失败列表
            # TODO 新建16位网段、方便下一次任务更新地址成功
            if ip == '0.0.0.0':
                return
            subnet16 = IPNetwork(f'{ip}/16').network
            subnet_16_instance = Subnet(subnet=str(subnet16) + "/16", mask=16,
                                        description=f'netops_ipam {file_time} 新建16位网段')
            subnet_16_instance.save()
            logger.info('请先创建此网段：{}'.format(ip))
            IpamMongoOps.post_fail_ip(ip)
            _tmp_data = []
            _tmp_data.append(ip + '\n')
            write_log(ip_am_ip_fail_file, _tmp_data)

    # IP地址当前已经存在Netops-IPAM中
    # 取值tag并更新tag
    # 更新在线时间
    # 更新描述信息 取消
    else:
        ip_address_id = ip_address_instance['id']
        ip_address_tag = ip_address_instance['tag']
        ip_address_desc = ip_address_instance.get('description', '{}')
        if ip_address_tag == 6:  # 已分配未使用变更到 >>> 已分配已使用 update 最近在线时间、描述信息
            # TODO 更新 6 >>> 2
            IpamMongoOps.post_update_ip(ip)
            ip_update_6_instance = IpAddress.objects.get(id=ip_address_id)
            ip_update_6_instance.tag = 2
            ip_update_6_instance.lastOnlineTime = lastOnlineTime
            ip_update_6_instance.description = ip_address_desc if ip_address_desc else tmp_description

            ip_update_6_instance.save()
        if ip_address_tag == 7:  # 自定义空闲变更到 >>> 未分配已使用、最近在线时间、描述信息
            # TODO 更新 7 >>> 4
            IpamMongoOps.post_update_ip(ip)
            ip_update_7_instance = IpAddress.objects.get(id=ip_address_id)
            ip_update_7_instance.tag = 4
            ip_update_7_instance.lastOnlineTime = lastOnlineTime
            ip_update_7_instance.description = tmp_description

            ip_update_7_instance.save()
        else:  # 更新tag、最近在线时间、描述信息
            # TODO 更新 未使用-仅更新在线时间、描述信息
            IpamMongoOps.post_update_ip(ip)
            ip_update_else_instance = IpAddress.objects.get(id=ip_address_id)
            ip_update_else_instance.tag = ip_address_tag
            ip_update_else_instance.lastOnlineTime = lastOnlineTime
            ip_update_else_instance.description = ip_address_desc if ip_address_desc else tmp_description
            ip_update_else_instance.save()

    return


# IPAM地址全网更新主任务main
@shared_task(base=QueueOnce, once={'graceful': True})
async def ip_am_update_main():
    task_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    start_time = time.time()
    logger.info("IPAM信息更新开始:{}".format(task_start_time))
    file_time = datetime.now().strftime("%Y-%m-%d")
    # 获取tasks任务数量
    ip_am_update_tasks = []
    # 获取现网中所有IP地址 Total_ip_list
    total_ip = IpamMongoOps.get_total_ip()
    # 保留失败的地址
    ip_am_ip_fail_file = os.path.join(BASE_DIR, 'media', 'ipam', "netops_ipam_ip_fail-{}.log".format(file_time))

    # 删除旧mongo数据库
    if total_ip:
        IpamMongoOps.delet_coll(coll='netops_ipam_fail_ip')
        IpamMongoOps.delet_coll(coll='netops_ipam_success_ip')
        IpamMongoOps.delet_coll(coll='netops_ipam_update_ip')
    else:
        return
    # TODO 数据量很大导致任务很慢-优化执行逻辑
    for ip_info in total_ip:
        if ip_info['ipaddress']:
            # logger.info(ip_info['ipaddress'])
            await ip_am_update_sub_task(ip_info.get("ipaddress", "0.0.0.0"))
            # ip_am_update_tasks.append(
            #     ip_am_update_sub_task.apply_async(args=(ip_info['ipaddress'],), queue='netops_ipam'))
    logger.info("子任务下发完毕")

    # 等待子任务全部执行结束后执行下一步
    while len(ip_am_update_tasks) != 0:
        for tasks in ip_am_update_tasks:
            if tasks.ready():
                ip_am_update_tasks.remove(tasks)
    logger.info('子任务执行完毕')
    total_time = int((time.time() - start_time) / 60)
    logger.info('花费总时间', total_time)

    ip_fail_counts = IpamMongoOps.get_coll_account(coll='netops_ipam_fail_ip')  # 失败地址表
    ip_add_counts = IpamMongoOps.get_coll_account(coll='netops_ipam_success_ip')  # 新增地址表
    ip_update_counts = IpamMongoOps.get_coll_account(coll='netops_ipam_update_ip')  # 更新地址表

    # 发送邮件和微信信息
    send_message = 'IPAM信息更新完成!\n新录入成功: {}个\n新录入失败: {}个\n更新成功: {}个\n总耗时: {}分钟\n'.format(
        ip_add_counts, ip_fail_counts, ip_update_counts, total_time)
    # 收件人邮箱
    email_addr = settings.EMAIL_RECEIVE_USER
    email_subject = 'IPAM信息更新结果_' + datetime.now().strftime("%Y-%m-%d %H:%M")
    email_text_content = send_message
    if os.path.exists(ip_am_ip_fail_file):
        send_mail(receive_email_addr=email_addr, email_subject=email_subject,
                  email_text_content=email_text_content, file_path=ip_am_ip_fail_file)
    else:
        send_mail(receive_email_addr=email_addr, email_subject=email_subject, email_text_content=email_text_content)

    # 最后获取任务结束时间
    task_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info("发送微信、邮件完毕:{}".format(task_end_time))

    return


# async+await异步模式
@shared_task(base=QueueOnce, once={'graceful': True})
def ipam_update_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ip_am_update_main())


# 定时回收地址
# 特定地址不回收？
'''
# 子网白名单

'''


# 地址回收任务
@shared_task(base=QueueOnce, once={'graceful': True})
def recycle_ip_main():
    # 近一天未在线、三天不在线、10天不在线、30天不在线、60天不在线、90天不在线
    start_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    start_message = f"IPAM回收任务开始, 开始时间: {start_time} "
    logger.info(start_message)
    # 获取media文件夹路径
    media_path = pathlib.Path(settings.MEDIA_ROOT)
    # IP地址回收文件夹名称
    folder_name = "netops_ip_address_recycle"

    # 拼接Excel 保存路径
    save_path = media_path / folder_name

    # 判断路径是否存在
    if not save_path.is_dir():
        try:
            # 获取绝对路径
            absolute_path = save_path.resolve()
            # 创建文件夹
            absolute_path.mkdir()
        except Exception as ex:
            raise RuntimeError("创建IP地址回收的目录失败!", ex)

        # 迭代目录内的xlsx文件数量,并按照文件创建的时间从高到低排序(先创建的文件在后面,后创建的文件在前面)
    excel_files = sorted([f for f in save_path.iterdir() if (str(f).endswith(".xlsx"))],
                         key=lambda x: os.path.getctime(x),
                         reverse=True, )

    # 按照文件创建的时间从高到低排序(先创建的文件在后面,后创建的文件在前面)
    # excel_files = [f for f in save_path.iterdir() if (str(f).endswith("xlsx"))]
    # excel_files.sort(key=lambda x: os.path.getctime(x), reverse=True)

    # 如果存储数量大于20,则删除掉最后一个文件
    if 20 <= len(excel_files):
        # 获取最后一个文件的路径
        last_file_path = excel_files[-1]
        # 删除最后一个文件
        os.remove(path=str(last_file_path))

    file_name = f"{start_time}地址回收报告.xlsx"
    full_path = f"{pathlib.Path(save_path) / file_name}"
    writer = pd.ExcelWriter(path=full_path)

    nine_days_ago_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    # 标注网段白名单
    subnet_white_list = [
        # 子网白名单

    ]
    # 获取所有网段列表-通过网段列表获取下面的ip地址
    offline_1_day = []
    offline_3_day = []
    offline_10_day = []
    offline_30_day = []
    offline_60_day = []
    offline_90_day = []
    whole_subnet_list = Subnet.objects.all()
    for subnet_instance in whole_subnet_list:
        # 排除特定网段
        if subnet_white_list not in subnet_white_list:
            ip_instance_list = subnet_instance.ipaddress_set.all()
            for ip_instance in ip_instance_list:
                last_online_time = ip_instance.lastOnlineTime
                # 对不在白名单的网段进行地址回收
                struct_date = datetime.strptime(str(last_online_time), "%Y-%m-%d")
                current_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
                time_delta = current_date - struct_date
                offline_days = time_delta.days
                if offline_days == 1:
                    logger.info(f" {ip_instance.ip_address} 离线时间为1天")
                    offline_1_day.append(ip_instance.ip_address)
                elif 3 == offline_days:
                    logger.info(f" {ip_instance.ip_address} 离线时间为3天")
                    offline_3_day.append(ip_instance.ip_address)
                elif 10 == offline_days:
                    logger.info(f" {ip_instance.ip_address} 离线时间为10天")
                    offline_10_day.append(ip_instance.ip_address)
                elif 30 == offline_days:
                    logger.info(f" {ip_instance.ip_address} 离线时间为30天")
                    offline_30_day.append(ip_instance.ip_address)
                elif 60 == offline_days:
                    logger.info(f" {ip_instance.ip_address} 离线时间为60天")
                    offline_60_day.append(ip_instance.ip_address)
                elif 90 <= offline_days:
                    logger.info(f" {ip_instance.ip_address} 离线时间大于90天")
                    # 重置标签为自定义空闲(tag=7)
                    # ipam.update_address(ip_address_id=id, tag=7)
                    offline_90_day.append(ip_instance.ip_address)
                    ip_instance.tag = 1
                    ip_instance.save()
            pass
    offline_1_day_df = pd.DataFrame(data=offline_1_day)
    offline_3_day_df = pd.DataFrame(data=offline_3_day)
    offline_10_day_df = pd.DataFrame(data=offline_10_day)
    offline_30_day_df = pd.DataFrame(data=offline_30_day)
    offline_60_day_df = pd.DataFrame(data=offline_60_day)
    offline_90_day_df = pd.DataFrame(data=offline_90_day)

    offline_1_day_df.index += 1
    offline_3_day_df.index += 1
    offline_10_day_df.index += 1
    offline_30_day_df.index += 1
    offline_60_day_df.index += 1
    offline_90_day_df.index += 1

    offline_1_day_df.to_excel(excel_writer=writer, sheet_name="offline_1_day", index=True)
    offline_3_day_df.to_excel(excel_writer=writer, sheet_name="offline_3_day", index=True)
    offline_10_day_df.to_excel(excel_writer=writer, sheet_name="offline_10_day", index=True)
    offline_30_day_df.to_excel(excel_writer=writer, sheet_name="offline_30_day", index=True)
    offline_60_day_df.to_excel(excel_writer=writer, sheet_name="offline_60_day", index=True)
    offline_90_day_df.to_excel(excel_writer=writer, sheet_name="offline_90_day_df", index=True)
    # 保存,生成文件
    writer.close()
    logger.info(f"{full_path} 保存成功!")
    # 最近在线时间为90天之前
    # TODO 且需要排除特定地址
    # recycle_ip_list = IpAddress.objects.filter(lastOnlineTime__lt=nine_days_ago_date)
    # for recycle in recycle_ip_list:
    #     recycle.tag = 1
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    end_message = f" IPAM回收任务结束, 结束时间: {end_time} "
    logger.info(end_message)

    # 发送邮件和微信信息
    send_message = ' IPAM回收完成!'
    email_addr = settings.EMAIL_RECEIVE_USER
    email_subject = ' IPAM回收结果_' + datetime.now().strftime("%Y-%m-%d %H:%M")
    email_text_content = send_message
    # if os.path.exists(save_path):
    send_mail(receive_email_addr=email_addr, email_subject=email_subject,
              email_text_content=email_text_content, file_path=full_path)
    # else:
    #     send_mail(receive_email_addr=email_addr, email_subject=email_subject, email_text_content=email_text_content)

    pass


#  特定网段新增描述信息
@shared_task(base=QueueOnce, once={'graceful': True})
def descript_special_subnet_task():
    task_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('特定网段描述更新开始', task_start_time)
    # special_subnet_list = get_special_subnet()
    special_subnet_list = []
    # 循环special_subnet_list 添加描述信息
    # 最后发送任务邮件和微信信息
    # 任务日志记录
    start_time_second = time.time()

    task_args = '特定网段描述更新:禁止操作:更新时间:' + task_start_time
    for subnet_instance in special_subnet_list:
        # logger.info(subnet_instance)
        subnet = Subnet.objects.filter(name=subnet_instance)
        subnet.update(description=task_args)
    # end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    email_addr = ['netaxe@netaxe.com']
    eend_time_second = time.time()
    email_subject = '特定网段描述更新结果_' + datetime.now().strftime("%Y-%m-%d %H:%M")
    cost_time = (eend_time_second - start_time_second)
    logger.info(f"特定网段新增描述信息 保存成功, 总耗时{round(cost_time)} 秒")

    message = "特定网段描述更新成功"
    email_text_content = message + ",本次特定描述更新成功网段数量:" + str(len(special_subnet_list))
    send_mail(receive_email_addr=email_addr, email_subject=email_subject, email_text_content=email_text_content)

    task_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logger.info('特定网段描述更新成功', task_end_time)
    logger.info(email_text_content)


if __name__ == '__main__':
    pass
    # import asyncio
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(ip_am_update_main())
