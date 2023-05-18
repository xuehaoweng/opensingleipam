import requests


def get_special_subnet():
    '''
    :return: ['10.100.187.0/24', '10.100.100.0/22', '10.100.25.0/24']
    '''
    res = []
    url = 'http://special-host:4346/api/xfapi/subnets?subnet_type=classical'
    r = requests.get(url)
    if r.status_code != 200:
        return r

    for i in r.json()['data']:
        # for j in i['classical']:
        #     res.append(j['cidr'])
        res.append(i['cidr'])

    url = 'http://172.16.59.94:4346/api/xfapi/subnets?subnet_type=ironic'
    r = requests.get(url)
    if r.status_code != 200:
        return r

    for i in r.json()['data']:
        res.append(i['cidr'])

    return res
