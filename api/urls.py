from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HardwareViewSet, InterfaceViewSet, DeviceViewSet, NetworkViewSet

router = DefaultRouter()
router.register(r'networks', NetworkViewSet, basename='Network')
router.register(r'interfaces', InterfaceViewSet, basename='Interface')
router.register(r'devices', DeviceViewSet, basename='Device')
router.register(r'hardware', HardwareViewSet, basename='Hardware')

urlpatterns = [
    path('', include(router.urls))
]
