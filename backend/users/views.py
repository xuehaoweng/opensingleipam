from django.shortcuts import render

# Create your views here.
# from django_filters import filters
from django import db
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, pagination, viewsets, permissions, filters

from users.models import OpLogs
from users.serializers import OpLogsSerializer
from utils.custom_pagination import LargeResultsSetPagination
from utils.custom_viewset_base import CustomViewBase


class OpLogsViewSet(CustomViewBase):
    db.connections.close_all()
    # subnet_model = Subnet
    permission_classes = ()
    queryset = OpLogs.objects.all().order_by('-id')
    serializer_class = OpLogsSerializer
    pagination_class = LargeResultsSetPagination
    # 配置搜索功能
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = '__all__'
