from django.urls import path, include
from rest_framework.routers import DefaultRouter

from open_ipam.views import SubnetHostsView, AvailableIpView, SubnetApiViewSet, IpAddressApiViewSet, SubnetAddressView, \
    IpAmSubnetTreeView, IpAmHandelView

# JobCenterView PeriodicTaskViewSet IntervalScheduleViewSet
router = DefaultRouter()
#
router.register(r'subnet_list', SubnetApiViewSet)  # 获取子网段列表
router.register(r'ip_address_list', IpAddressApiViewSet)
# router.register(r'periodic_task', PeriodicTaskViewSet)
# router.register(r'interval_schedule', IntervalScheduleViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    # path(r'api/', include(router.urls)),
    # path('jobCenter/', JobCenterView.as_view(), name='jobCenter'),
    path('subnet_tree/', IpAmSubnetTreeView.as_view(), name='subnet_tree'),
    path('address_handel/', IpAmHandelView.as_view(), name='address_handel'),

    path('subnet/<str:subnet_id>/ip_address/', SubnetAddressView.as_view(), name='subnet_ip_address'),

    # 供admin后台展示，暂未修改过多逻辑
    path('subnet/<str:subnet_id>/hosts/', SubnetHostsView.as_view(), name='hosts'),
    # path('subnet/<str:subnet_id>/hosts/', SubnetHostsView.as_view(), name='hosts'),
    path(
        'subnet/<str:subnet_id>/get-next-available-ip/',
        AvailableIpView.as_view(),
        name='get_next_available_ip',
    ),
]
