# phpipam 数据同步
import requests
from requests.auth import HTTPBasicAuth

from confload.confload import config


class PhpIpamApi():
    def __init__(self):
        self.base_url = config.phpipam_url
        self.data = {
            "username": config.phpipam_username,
            "password": config.phpipam_password,
        }
        self.auth = HTTPBasicAuth(self.data['username'], self.data['password'])
        self.token = self.get_token()
        self.headers = {
            "Content-Type": "application/json",
            "token": str(self.token['data']['token']),
        }

    def get_token(self):
        get_token_url = self.base_url + "/api/myapp/user/token/"
        headers = {
            "Content-Type": "application/json"
        }
        r = requests.post(get_token_url, auth=self.auth, headers=headers)
        return r.json()

    # 获取所有已分配子网信息
    def get_all_subnets(self):
        all_subnets_url = self.base_url + "/api/myapp/subnets/"
        response = requests.get(all_subnets_url, headers=self.headers)
        subnets_info = response.json()
        if subnets_info['code'] == 200:
            return subnets_info['data']

    def get_all_addresses(self):
        all_addresses_url = self.base_url + "/api/myapp/addresses/"
        response = requests.get(all_addresses_url, headers=self.headers)
        ipaddress_info = response.json()
        if ipaddress_info['code'] == 200:
            return ipaddress_info['data']

    def get_all_addresses_by_subnet(self):
        all_subnets = self.get_all_subnets()
        # 网段下的所有地址
        subnet_addresses = []
        # 循环所有网段
        for subnet_info in all_subnets:  # [:11],测试
            tmp = {}
            subnet_id = subnet_info['id']
            # 获取此网段所有IP地址明细[{},{}]
            subnet_ipaddress_url = self.base_url + "api/myapp/subnets/{}/addresses/".format(subnet_id)
            r = requests.get(subnet_ipaddress_url, headers=self.headers)
            if r.ok:
                if r.json()['code'] == 200 and r.json()['success'] == True:
                    tmp[subnet_info['subnet'] + '/' + subnet_info['mask']] = r.json()['data']
                    # print(tmp)
                    subnet_addresses.append(tmp)
            else:
                # phpipam地址同步：网段下无地址或异常-该网段不处理
                print('查询网段下的IP异常', subnet_info['subnet'])
                pass

        return subnet_addresses

    def get_address_by_subnet_instance(self, subnet_instance):
        # 网段下的所有地址
        address_list = []
        tmp = {}
        # 获取此网段所有IP地址明细[{},{}]
        subnet_ipaddress_url = self.base_url + "api/myapp/subnets/{}/addresses/".format(subnet_instance['id'])
        addr_res = requests.get(subnet_ipaddress_url, headers=self.headers)
        if addr_res.ok:
            if addr_res.json()['code'] == 200 and addr_res.json()['success'] == True:
                address_res_list = addr_res.json()['data']
                address_list = address_res_list
        else:
            # phpipam地址同步：网段下无地址或异常-该网段不处理
            print('查询网段下的IP异常', subnet_instance['subnet'])
            pass

        return address_list
