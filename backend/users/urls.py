from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import OpLogsViewSet

router = DefaultRouter()
router.register(r'oplogs', OpLogsViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
]
