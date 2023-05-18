# phpipam 数据同步
import requests
from requests.auth import HTTPBasicAuth

ipam = {
    "url": "http://10.254.0.115/",
    "username": "netops_api",
    "password": "KlpR9qUm3a",
}


class PhpIpamApi():
    def __init__(self):
        self.base_url = ipam['url']
        self.data = {
            "username": ipam['username'],
            "password": ipam['password'],
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
                print('查询网段下的IP异常', subnet_info['subnet'])
                pass

        return subnet_addresses
