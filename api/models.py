from django.db import models


class Hardware(models.Model):
    name = models.CharField(max_length=50)
    recommended_os_version = models.CharField(max_length=50)
    capabilities = models.CharField(max_length=200)
    number_of_interfaces = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Device(models.Model):
    ROLES = (
        ('access', 'access'),
        ('distribution', 'distribution'),
        ('core', 'core'),
        ('edge', 'edge'),
    )

    name = models.CharField(max_length=30)
    management_address = models.GenericIPAddressField()
    hardware_model = models.ForeignKey(Hardware,
                                       on_delete=models.CASCADE,
                                       related_name='devices',
                                       null=False)
    device_role = models.CharField(max_length=20,
                                   choices=ROLES)

    def __str__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=30)
    network_address = models.GenericIPAddressField()
    subnet_mask = models.PositiveIntegerField()
    vlan_tag = models.PositiveIntegerField()
    gateway = models.ForeignKey(Device,
                                on_delete=models.CASCADE,
                                related_name='networks')

    def __str__(self):
        return self.name


class Interface(models.Model):
    name = models.CharField(max_length=50)
    device = models.ForeignKey(Device,
                               on_delete=models.CASCADE,
                               related_name='interfaces')
    connected_to = models.OneToOneField('self',
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True)

    def __str__(self):
        return self.name
