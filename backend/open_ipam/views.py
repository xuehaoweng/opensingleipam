import json
import time

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from netaddr import iter_iprange
from rest_framework import serializers, filters
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from open_ipam.models import Subnet, IpAddress, TagsModel
from open_ipam.serializers import HostsResponseSerializer, SubnetSerializer, IpAddressSerializer, \
    TagsModelSerializer
from open_ipam.tools.ipam_pagenations import HostsListPagination
from utils.custom_pagination import LargeResultsSetPagination
from utils.custom_viewset_base import CustomViewBase
from utils.ipam_utils import IpAmForNetwork
import ipaddr


# 定义host 响应 返回值字段
class HostsResponse(object):
    def __init__(self, address, used, tag, subnet, lastOnlineTime, description):
        # def __init__(self, address, used, tag, subnet):
        self.address = address
        self.used = used
        self.tag = tag
        self.subnet = subnet
        self.lastOnlineTime = lastOnlineTime
        self.description = description


class HostsSet:
    model = Subnet

    def __init__(self, subnet, start=0, stop=None):
        self.start = start
        self.stop = stop
        self.subnet = subnet
        self.network = int(self.subnet.subnet.network_address)
        self.used_set = subnet.ipaddress_set.all()

    def __getitem__(self, i):
        # 如果传递进来的参数i是一个切片对象，则获取start和stop的值
        if isinstance(i, slice):
            start = i.start
            stop = i.stop
            # 如果 start 或 stop 是 None，说明切片的开始或结束位置没有被指定，那么就将其赋值为 0 或 self.count()
            if start is None:  # pragma: no cover
                start = 0
            if stop is None:  # pragma: no cover
                stop = self.count()
            # 如果 stop 的值超过了索引的范围，那么就将其赋值为 self.count()。
            else:
                stop = min(stop, self.count())
            return HostsSet(self.subnet, self.start + start, self.start + stop)
        # 如果索引超出count 则报index错
        if i >= self.count():
            raise IndexError
        # Host starts from next address生成一个 IP 地址对象

        ip_address_instance = self.subnet.subnet._address_class(self.network + 1 + i + self.start)
        # print()
        # In case of single hosts ie subnet/32 & /128
        if self.subnet.subnet.prefixlen in [32, 128]:
            ip_address_instance = ip_address_instance - 1
        # 判断Ip地址是否存在，编辑使用与否
        used = self.used_set.filter(ip_address=str(ip_address_instance)).exists()
        # 默认tag为1
        tag = 1

        host_instance = self.used_set.filter(ip_address=str(ip_address_instance)).first()
        # 如果已经被使用，需要判断实际的tag是什么
        if used:
            tag = host_instance.tag
        # 描述和最近在线时间

        description = ''
        lastOnlineTime = ''

        if host_instance:
            description = host_instance.description
            lastOnlineTime = host_instance.lastOnlineTime

        return HostsResponse(str(ip_address_instance), used, tag, self.subnet, lastOnlineTime, description)

    # 计算当前subnet的实际可用地址是多少
    def count(self):
        if self.stop is not None:
            return self.stop - self.start
        broadcast = int(self.subnet.subnet.broadcast_address)

        # IPV4
        if self.subnet.subnet.version == 4:
            # Networks with a mask of 32 will return a list
            # containing the single host address
            if self.subnet.subnet.prefixlen == 32:
                return 1
            # Other than subnet /32, exclude broadcast
            return broadcast - self.network - 1
        # IPV6
        else:
            # Subnet/128 only contains single host address
            if self.subnet.subnet.prefixlen == 128:
                return 1
            return broadcast - self.network

    def __len__(self):
        return self.count()

    def index_of(self, address):
        index = int(self.subnet.subnet._address_class(address)) - self.network - 1
        if index < 0 or index >= self.count():  # pragma: no cover
            raise serializers.ValidationError({'detail': _('Invalid Address')})
        return index


# class ProtectedAPIMixin(object):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]
#     throttle_scope = 'ipam'

# ProtectedAPIMixin
class SubnetHostsView(ListAPIView):
    subnet_model = Subnet
    queryset = Subnet.objects.none()
    serializer_class = HostsResponseSerializer
    pagination_class = HostsListPagination

    def get_queryset(self):
        super().get_queryset()
        # get subnet instance
        subnet = get_object_or_404(self.subnet_model, pk=self.kwargs['subnet_id'])
        queryset = HostsSet(subnet)
        return queryset


# 获取可用I配置
class AvailableIpView(RetrieveAPIView):
    subnet_model = Subnet
    queryset = IpAddress.objects.none()
    serializer_class = serializers.Serializer

    def get(self, request, *args, **kwargs):
        subnet = get_object_or_404(self.subnet_model, pk=self.kwargs['subnet_id'])
        print(subnet)
        return Response(subnet.get_next_available_ip())


# 子网网段API
class SubnetApiViewSet(CustomViewBase):
    # subnet_model = Subnet
    permission_classes = ()
    queryset = Subnet.objects.all().order_by('-id')
    serializer_class = SubnetSerializer
    pagination_class = LargeResultsSetPagination
    # 配置搜索功能
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('mask', 'name')


# IP地址Api
class IpAddressApiViewSet(CustomViewBase):
    # subnet_model = Subnet
    # permission_classes = ()
    queryset = IpAddress.objects.all().order_by('-id')
    serializer_class = IpAddressSerializer
    pagination_class = LargeResultsSetPagination
    # 配置搜索功能
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = '__all__'


class SubnetAddressView(ListAPIView):
    subnet_model = Subnet
    queryset = Subnet.objects.none()
    serializer_class = HostsResponseSerializer
    pagination_class = HostsListPagination

    def get_queryset(self):
        # start_time = time.time() * 1000
        super().get_queryset()
        subnet_instance = Subnet.objects.get(id=self.kwargs['subnet_id'])
        queryset = HostsSet(subnet_instance)
        return queryset


# 获取 get subnet_tree
class IpAmSubnetTreeView(APIView):
    def get(self, request):
        get_params = request.GET.dict()
        if 'subnet' in get_params:
            ip_am_network = IpAmForNetwork()
            res_list = list(Subnet.objects.all().order_by('subnet').values())
            # 处理树结构返回前端
            tree = ip_am_network.generate_netops_tree(res_list)
            res = {'data': tree, 'code': 200, }
            return JsonResponse(res, safe=True)
        if "tags" in get_params:
            tag_choices = TagsModel.objects.all()
            tags = TagsModelSerializer(tag_choices, many=True)
            res = {'data': tags.data, 'code': 200, 'count': len(tags.data)}
            return JsonResponse(res, safe=True)


# 地址操作 增删改查
class IpAmHandelView(APIView):
    def post(self, request):
        update = request.POST.get('update')
        range_update = request.POST.get('range_update')
        delete = request.POST.get('delete')
        subnet_id = request.POST.get('subnet_id')
        description = request.POST.get('description')
        add_subnet = request.POST.get('add_subnet')
        add_description = request.POST.get('add_description')
        add_master_id = request.POST.get('add_master_id')
        room_group_name = request.POST.get('room_group_name')
        if update:
            update_list = json.loads(update)
            for update_info in update_list:
                IpAddress.objects.update_or_create(ip_address=update_info['ipaddr'], tag=update_info['tag'],
                                                   description=update_info['description'],
                                                   subnet_id=update_info['subnet_id'])
            res = {'message': '地址分配成功', 'code': 200, 'update_ip_list': [j['ipaddr'] for j in update_list]}
            return JsonResponse(res, safe=True)
        if range_update:
            range_data = json.loads(range_update)
            print(range_data)
            start_ip = range_data['start_ip']
            end_ip = range_data['end_ip']
            description = range_data['description']
            subnet_id = range_data['subnet_id']
            update_ip_list = []
            for host_ip in iter_iprange(start_ip, end_ip):
                # print(host_ip)

                IpAddress.objects.update_or_create(ip_address=str(host_ip), tag=range_data['tag'],
                                                   description=description,
                                                   subnet_id=subnet_id)
                update_ip_list.append(str(host_ip))

            res = {'message': '地址批量分配成功', 'code': 200, 'update_ip_list': update_ip_list}
            return JsonResponse(res, safe=True)
        if delete:
            delete_ip_list = json.loads(delete)
            print(delete_ip_list)
            for delete_info in delete_ip_list:
                IpAddress.objects.filter(ip_address=delete_info['ipaddr']).delete()
            res = {'message': '地址回收成功', 'code': 200, 'delete_ip_list': [j['ipaddr'] for j in delete_ip_list]}
            return JsonResponse(res, safe=True)

        if description:
            Subnet.objects.update(description=description)
            res = {'message': '网段描述更新成功', 'code': 200, }
            return JsonResponse(res, safe=True)

        if add_subnet:
            try:
                # print(add_master_id, type(add_master_id))
                master_subnet_id = Subnet.objects.filter(id=int(add_master_id)).first()
                add_kwargs = {
                    "name": add_subnet,
                    "mask": add_subnet.split("/")[1],
                    "subnet": add_subnet,
                    "description": add_description,
                    "master_subnet": master_subnet_id
                }
                subnet_list = [str(i.subnet) for i in Subnet.objects.all()]
                if add_master_id == "0":
                    add_kwargs.pop('master_subnet')
                    if add_subnet in subnet_list:
                        res = {'message': '新增网段失败,当前新增网段已经存在', 'code': 400, }
                    else:
                        Subnet.objects.update_or_create(**add_kwargs)
                        res = {'message': '新增网段成功', 'code': 200, }
                    return JsonResponse(res, safe=True)
                else:
                    master_subnet = Subnet.objects.get(id=add_master_id)
                    if str(master_subnet.subnet) == str(add_subnet):
                        res = {'message': '新增网段失败,请校验参数,不能新建跟父节点相同的子网段', 'code': 400, }
                        return JsonResponse(res, safe=True)
                    else:
                        # 校验IPV6
                        if ":" in str(master_subnet.subnet):

                            v6_master_subnet_detail = ipaddr.IPv6Network(str(master_subnet.subnet))
                            v6_add_subnet_detail = ipaddr.IPv6Network(str(str(add_subnet)))
                            if v6_add_subnet_detail in v6_master_subnet_detail:
                                if add_subnet in subnet_list:
                                    res = {'message': '新增网段失败,当前新增网段已经存在', 'code': 400, }
                                else:
                                    Subnet.objects.update_or_create(**add_kwargs)
                                    res = {'message': '新增网段成功', 'code': 200, }
                                return JsonResponse(res, safe=True)
                        # 校验IPV4
                        v4_master_subnet_detail = ipaddr.IPv4Network(str(master_subnet.subnet))
                        v4_add_subnet_detail = ipaddr.IPv4Network(str(str(add_subnet)))
                        if v4_add_subnet_detail in v4_master_subnet_detail:
                            if add_subnet in subnet_list:
                                res = {'message': '新增网段失败,当前新增网段已经存在', 'code': 400, }
                            else:
                                Subnet.objects.update_or_create(**add_kwargs)
                                res = {'message': '新增网段成功', 'code': 200, }

                        else:
                            res = {'message': '新增网段失败,请校验网段归属', 'code': 400, }
                        return JsonResponse(res, safe=True)
                # print(add_kwargs)
                # 校验是否有归属关系

                # print(str(master_subnet.subnet))
                # print(str(add_subnet))
                # print(str(add_subnet) == str(add_subnet))
                # 判断是否和父节点一致
            except Exception as e:
                res = {'message': e, 'code': 400, }
                return JsonResponse(res, safe=True)
