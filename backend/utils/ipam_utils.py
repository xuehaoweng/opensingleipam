# IPAM接口输出到运营平台
from open_ipam.models import Subnet
from netaddr import IPNetwork, IPSet


class IpAmForNetwork(object):

    # 根据给定的一系列子网信息，自动生成树
    def generate_tree(self, some_subnets):
        '''
        :param some_subnets: 一系列子网信息
        :return: 一个4层树结构
        '''
        res_list = some_subnets
        res_list_cp = res_list.copy()
        # print(res_list)
        no1_id_list = []  # 存放第一层子网的ipam_id
        no1_list = []  # 存放第一层子网的详细信息
        no2_id_list = []
        no2_list = []
        no3_id_list = []
        no3_list = []
        no4_id_list = []
        no4_list = []
        for i in res_list:
            if i['masterSubnetId'] == 0:
                no1_id_list.append(i['ipam_id'])
                tmp = {}
                tmp['id'] = i['ipam_id']
                tmp['masterSubnetId'] = i['masterSubnetId']
                tmp['label'] = i['ipName']
                tmp['children'] = []
                no1_list.append(tmp)
                res_list_cp.remove(i)

        # print(len(no1_id_list), len(res_list_cp))

        for i in res_list:
            if i['masterSubnetId'] in no1_id_list:
                no2_id_list.append(i['ipam_id'])
                tmp = {}
                tmp['id'] = i['ipam_id']
                tmp['masterSubnetId'] = i['masterSubnetId']
                tmp['label'] = i['ipName']
                tmp['children'] = []
                no2_list.append(tmp)
                res_list_cp.remove(i)

        print(len(no2_id_list), len(res_list_cp))

        for i in res_list:
            if i['masterSubnetId'] in no2_id_list:
                no3_id_list.append(i['ipam_id'])
                tmp = {}
                tmp['id'] = i['ipam_id']
                tmp['masterSubnetId'] = i['masterSubnetId']
                tmp['label'] = i['ipName']
                tmp['children'] = []
                no3_list.append(tmp)
                res_list_cp.remove(i)

        print(len(no3_id_list), len(res_list_cp))

        for i in res_list:
            if i['masterSubnetId'] in no3_id_list:
                no4_id_list.append(i['ipam_id'])
                tmp = {}
                tmp['id'] = i['ipam_id']
                tmp['masterSubnetId'] = i['masterSubnetId']
                tmp['label'] = i['ipName']
                tmp['children'] = []
                no4_list.append(tmp)
                res_list_cp.remove(i)

        print(len(no4_id_list), len(res_list_cp))

        for i in no3_list:
            for j in no4_list:
                if j["masterSubnetId"] == i["id"]:
                    i['children'].append(j)

        for i in no2_list:
            for j in no3_list:
                if j["masterSubnetId"] == i["id"]:
                    i['children'].append(j)

        for i in no1_list:
            for j in no2_list:
                if j["masterSubnetId"] == i["id"]:
                    i['children'].append(j)

        # no1_list = sorted(no1_list, key=lambda e: e['id'], reverse=False)

        return no1_list

    def generate_netops_tree(self, some_subnets):
        '''
        :param some_subnets: 一系列子网信息
        :return: 一个5层树结构
        '''
        res_list = some_subnets
        res_list_cp = res_list.copy()
        # print(res_list)
        no1_id_list = []  # 存放第一层子网的ipam_id
        no1_list = []  # 存放第一层子网的详细信息
        no2_id_list = []
        no2_list = []
        no3_id_list = []
        no3_list = []
        no4_id_list = []
        no5_id_list = []
        no6_id_list = []
        no4_list = []
        no5_list = []
        no6_list = []

        for e in res_list:
            # master_subnet_id为空--一级结构
            if e['master_subnet_id'] is None:
                no1_id_list.append(e['id'])
                tmp = {}
                tmp['id'] = e['id']
                tmp['master_subnet_id'] = e['master_subnet_id']
                tmp['network_type'] = e['network_type']
                tmp['label'] = str(e['subnet'])
                tmp['children'] = []
                no1_list.append(tmp)
                res_list_cp.remove(e)

        # print(len(no1_id_list), len(res_list_cp))
        # print(no1_id_list)

        for second in res_list:
            if second['master_subnet_id'] in no1_id_list:
                no2_id_list.append(second['id'])
                tmp = {}
                tmp['id'] = second['id']
                tmp['master_subnet_id'] = second['master_subnet_id']
                tmp['network_type'] = second['network_type']
                tmp['label'] = str(second['subnet'])
                tmp['children'] = []
                no2_list.append(tmp)
                res_list_cp.remove(second)

        # print(len(no2_id_list), len(res_list_cp))

        for third in res_list:
            if third['master_subnet_id'] in no2_id_list:
                no3_id_list.append(third['id'])
                tmp = {}
                tmp['id'] = third['id']
                tmp['master_subnet_id'] = third['master_subnet_id']
                tmp['network_type'] = third['network_type']
                tmp['label'] = str(third['subnet'])
                tmp['children'] = []
                no3_list.append(tmp)
                res_list_cp.remove(third)

        # print(len(no3_id_list), len(res_list_cp))

        for four in res_list:
            if four['master_subnet_id'] in no3_id_list:
                no4_id_list.append(four['id'])
                tmp = {}
                tmp['id'] = four['id']
                tmp['master_subnet_id'] = four['master_subnet_id']
                tmp['network_type'] = four['network_type']
                tmp['label'] = str(four['subnet'])
                tmp['children'] = []
                no4_list.append(tmp)
                res_list_cp.remove(four)
        for five in res_list:
            if five['master_subnet_id'] in no4_id_list:
                no5_id_list.append(five['id'])
                tmp = {}
                tmp['id'] = five['id']
                tmp['master_subnet_id'] = five['master_subnet_id']
                tmp['network_type'] = five['network_type']
                tmp['label'] = str(five['subnet'])
                tmp['children'] = []
                no5_list.append(tmp)
                res_list_cp.remove(five)

        for six in res_list:
            if six['master_subnet_id'] in no5_id_list:
                no6_id_list.append(six['id'])
                tmp = {}
                tmp['id'] = six['id']
                tmp['master_subnet_id'] = six['master_subnet_id']
                tmp['network_type'] = six['network_type']
                tmp['label'] = str(six['subnet'])
                tmp['children'] = []
                no6_list.append(tmp)
                res_list_cp.remove(six)
        # print(len(no4_id_list), len(res_list_cp))
        for i in no5_list:
            for j in no6_list:
                if j["master_subnet_id"] == i["id"]:
                    i['children'].append(j)
        for i in no4_list:
            for j in no5_list:
                if j["master_subnet_id"] == i["id"]:
                    i['children'].append(j)
        for i in no3_list:
            for j in no4_list:
                if j["master_subnet_id"] == i["id"]:
                    i['children'].append(j)

        for i in no2_list:
            for j in no3_list:
                if j["master_subnet_id"] == i["id"]:
                    i['children'].append(j)

        for i in no1_list:
            for j in no2_list:
                if j["master_subnet_id"] == i["id"]:
                    i['children'].append(j)

        # no1_list = sorted(no1_list, key=lambda e: e['id'], reverse=False)

        return no1_list

    # 根据给定的一系列子网信息，自动生成树-2022.05.31 TODO:结果是dict结构
    def build_tree_recursive(self, node_list, parent=None):
        '''
        :param node_list: all_subnets = list(IpamSubnet.objects.all().values('ipam_id', 'master_subnet_id', 'ipName'))
        :param parent: {'ipam_id': 0, 'master_subnet_id': None, 'ipName': '0.0.0.0/0'}
        :return:
        '''
        if not parent:
            parent = {'ipam_id': 0, 'master_subnet_id': None, 'ipName': '0.0.0.0/0'}
        children = []
        for i in node_list:
            if i.get('master_subnet_id') == parent['ipam_id']:
                children.append(i)

        parent['children'] = children

        for j in children:
            self.build_tree_recursive(node_list, parent=j)

        return parent

    #  返回树结构，所有子网
    def ipam_tree_all(self):
        # 获取总数
        all_subnets = Subnet.objects.all().values('id', 'master_subnet_id', 'name')
        res_list = list(all_subnets)
        res_list = [dict(t) for t in set([tuple(d.items()) for d in res_list])]
        res_list = sorted(res_list, key=lambda e: e['id'], reverse=False)

        tree = self.generate_tree(res_list)

        return tree

    #  # 为叶子节点，生成树结构
    def leaf_tree(self, leaf_node, all_subnets):
        res = [leaf_node]
        while leaf_node['master_subnet_id'] > 0:
            for i in all_subnets:
                if i['ipam_id'] == leaf_node['master_subnet_id']:
                    leaf_node = i
                    # print(leaf_node)
                    # res.append(leaf_node)
                    res.insert(0, leaf_node)
            else:
                break

        return res

    #  返回树结构,基于指定BGBU
    def ipam_tree_by_bgbu(self, bgbu_id):
        '''
        :param bgbu_id: [2,4,6,14]这样的列表信息
        '''
        pass

    def ipam_tree(self, bgbu=None):
        '''
        :param bgbu_id: [2,4,6,14]这样的列表信息
        '''
        if bgbu:
            tree = self.ipam_tree_by_bgbu(bgbu)
        else:
            tree = self.ipam_tree_all()

        return tree

    def get_sixteen_subnet_id(ip):
        # 排除ipv6地址同步操作
        if ":" not in ip:
            try:
                ip_mask = "{}/{}".format(ip, 16)
                subnet = "{}/{}".format(IPNetwork(ip_mask).network, 16)
                res = Subnet.objects.filter(subnet=subnet).values().first()
                if res:
                    return res['id']
            except Exception as e:
                return
        else:
            return
