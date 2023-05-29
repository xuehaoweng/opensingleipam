
from openwisp_utils.api.serializers import ValidatedModelSerializer
from rest_framework import serializers

from open_ipam.models import IpAddress, Subnet, TagsModel


class IpRequestSerializer(ValidatedModelSerializer):
    class Meta:
        model = IpAddress
        fields = ('subnet', 'description')
        # read_only_fields = ('created', 'modified')


class TagsModelSerializer(ValidatedModelSerializer):
    class Meta:
        model = TagsModel
        fields = '__all__'
        # read_only_fields = ('created', 'modified')


class IpAddressSerializer(ValidatedModelSerializer):
    class Meta:
        model = IpAddress
        fields = '__all__'
        # read_only_fields = ('created', 'modified')


class SubnetSerializer(ValidatedModelSerializer):
    master_subnet_name = serializers.CharField(source='subnet.name', read_only=True)

    class Meta:
        model = Subnet
        fields = '__all__'
        # read_only_fields = ('created', 'modified')


class ImportSubnetSerializer(serializers.Serializer):
    csvfile = serializers.FileField()


class HostsResponseSerializer(serializers.Serializer):
    address = serializers.CharField()
    used = serializers.BooleanField()
    tag = serializers.IntegerField()
    subnet = serializers.CharField()

    description = serializers.CharField()
    lastOnlineTime = serializers.DateField()


