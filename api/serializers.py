from rest_framework import serializers
from ipaddress import ip_address, ip_network
from .models import Hardware, Network, Device, Interface


class HardwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hardware
        fields = '__all__'


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'

    def validate_network_address(self, value):
        try:
            ip_address(value)
            return value
        except ValueError:
            raise serializers.ValidationError('Invalid ip address value')

    def validate_subnet_mask(self, value):
        if value in range(1, 33):
            return value
        else:
            raise serializers.ValidationError('Invalid subnet mask value')

    def validate_vlan_tag(self, value):
        if value in range(1, 4096):
            return value
        else:
            raise serializers.ValidationError('Invalid vlan tag value')

    def validate(self, request):
        address = request.data['network_address']
        mask = request.data['subnet_mask']
        try:
            ip_network(address + '/' + mask)
            return request
        except ValueError:
            raise serializers.ValidationError(f'{address}/{mask} is not a valid network address')


class DeviceSerializer(serializers.ModelSerializer):

    hardware_model = serializers.SlugRelatedField(many=False,
                                                  slug_field='name',
                                                  queryset=Hardware.objects.all())

    networks = NetworkSerializer(many=True,
                                 read_only=True)

    interfaces = serializers.PrimaryKeyRelatedField(many=True,
                                                    read_only=True)

    class Meta:
        model = Device
        fields = '__all__'

    def validate_management_address(self, value):
        try:
            ip_address(value)
            return value
        except ValueError:
            raise serializers.ValidationError('Invalid management ip address')


class InterfaceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    device = serializers.StringRelatedField(read_only=True)
    # Field custom(nu exista in model), definit printr-o metoda
    device_id = serializers.SerializerMethodField(source='get_device_id')

    class Meta:
        model = Interface
        fields = '__all__'

    def get_device_id(self, obj):
        return obj.device.id
