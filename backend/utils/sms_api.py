#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Author_ HW
# Filename: SMS_API.py

import requests
import hashlib
import string
import time
import json
from datetime import datetime


class SmsApi():
    def __init__(self):
        self.version = "1.0"
        self.X_IFLYFDP_USER = 'CCR_NETWORK'
        self.Auth_PWD = '569981977501569'
        self.X_IFLYFDP_TS = str(int(time.time()))
        self.X_IFLYFDP_NONCE = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.X_IFLYFDP_TOKEN = get_md5(self.Auth_PWD + self.X_IFLYFDP_NONCE + self.X_IFLYFDP_TS).upper()
        self.url = 'http://fdpapi.adsring.cn'
        self.headers = self.node_headers()

    def node_headers(self):
        headers = {
            'X-IFLYFDP-USER': self.X_IFLYFDP_USER,
            'X-IFLYFDP-TS': self.X_IFLYFDP_TS,
            'X-IFLYFDP-NONCE': self.X_IFLYFDP_NONCE,
            'X-IFLYFDP-TOKEN': self.X_IFLYFDP_TOKEN,
            # "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        return headers

    # 查询账户余额接口
    def get_smsBalance(self):
        url = 'http://fdpapi.adsring.cn/account/queryBalance'
        try:
            resp = requests.post(url, headers=self.headers, timeout=10)
            # print(resp.status_code)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            # print(e)
            pass

        return {}

    #
    def send_sms(self, telNo, message):
        url = 'http://fdpapi.adsring.cn/sms/order/1'
        smsParam = {
            'message': message,
        }
        body = {
            'telNo': telNo,
            'smsType': int(0),
            'smsSignId': int(1),
            'smsTemplateId': int(143713140424530),
            'smsParam': json.dumps(smsParam),
        }

        try:
            resp = requests.post(url, headers=self.headers, data=body)
            # print('status_code:',resp.status_code)
            # print('text:',resq.text)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            # print(e)
            pass

        return {}

    def search_smsResult(self, platOrderId):
        url = 'http://fdpapi.adsring.cn/flow/queryOrder'
        body = {
            'platOrderId': platOrderId,
        }
        try:
            resp = requests.post(url, headers=self.headers, data=body)
            # print('status_code:',resp.status_code)
            # print('text:',resp.text)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            # print(e)
            pass

        return {}


def get_md5(md5_txt):
    """
    用于获取字符串的md5值
    md5_txt：字符串内容
    return: md5码，32位
    """
    md5 = hashlib.md5()
    md5.update(md5_txt.encode('utf-8'))
    return md5.hexdigest()


def tx_sms(msg: str, iphone: list):
    url = "http://dcsms.msg.com/api/ten/tencentcloud/tencloudsms.action"

    payload = {'uuid': '***********',
               'params': str([msg]),
               'type_num': '2',
               'iphone': str(iphone)}
    files = [

    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text


def test_main():
    # 查账户余额测试
    _sms = SmsApi()
    res = _sms.get_smsBalance()
    # res = {'returnCode': '0000', 'returnDesc': '成功', 'data': {'balance': 294}}
    # # res = {'returnCode': 'a001', 'returnDesc': '请求不符合鉴权规则ip 36.7.144.39 不被授权调用接口.', 'data': None}
    # # print(res)
    if res['returnCode'] != '0000':
        # print(res)
        print("查询时间：{}\n查询结果：{}\n账户余额：{}\n".format(datetime.now(), res['returnDesc'], res['data']))
    else:
        # print("查询时间：{}\n查res['returnDesc'],res['data']询结果：{}\n账户余额：{}分\n".format(datetime.now(),res['returnDesc'],res['data']))
        print("查询时间：{}\n查询结果：{}\n账户余额：{}分\n".format(datetime.now(), res['returnDesc'], res['data']['balance']))

    # 发短信测试
    '''{'returnCode': '0000', 'returnDesc': '成功', 'data': {'batchSeriesId': 11111111, 'details': [{'telNo': '1111111', 'customerOrderId': '', 'platOrderId': 1111111}]}}'''
    telNo = '111111111,1111111111'
    message = '短信接口测试内容'
    _sms = SmsApi()
    res1 = _sms.send_sms(telNo, message)

    print(res1)

    # 短信发送结果查询测试
    # platOrderId = '2300173368391009'
    # _sms = SmsApi()
    # res2 = _sms.search_smsResult(platOrderId)
    # print(res2)


if __name__ == "__main__":
    tx_sms("test1122", ["1111111111"])

    pass
