from rest_framework import viewsets, mixins

from .models import Device, Hardware, Network, Interface
from .pagination import StandardResultSetPagination, InterfaceResultSetPagination
from .permissions import AdminAllAuthenticatedReadOnly
from .serializers import DeviceSerializer, HardwareSerializer, NetworkSerializer, InterfaceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    # warning legat de paginare daca nu este ordonat queryset-ul si e folosit objects.all()
    queryset = Device.objects.order_by('id')
    model = Device
    serializer_class = DeviceSerializer
    permission_classes = [AdminAllAuthenticatedReadOnly]
    pagination_class = StandardResultSetPagination


class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.order_by('id')
    model = Hardware
    serializer_class = HardwareSerializer
    permission_classes = [AdminAllAuthenticatedReadOnly]
    pagination_class = StandardResultSetPagination


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.order_by('id')
    model = Network
    serializer_class = NetworkSerializer
    permission_classes = [AdminAllAuthenticatedReadOnly]
    pagination_class = StandardResultSetPagination


class InterfaceViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):
    """
    Custom view set - accepta metodele GET & PUT
    Interfetele sunt create/sters la crearea/stergerea unui Device (utilizeaza semnale - signals.py)
    """
    queryset = Interface.objects.order_by('id')
    model = Interface
    serializer_class = InterfaceSerializer
    permission_classes = [AdminAllAuthenticatedReadOnly]
    pagination_class = InterfaceResultSetPagination
