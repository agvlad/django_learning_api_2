from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Device, Interface


@receiver(post_save, sender=Device)
def create_interfaces(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.hardware_model.number_of_interfaces):
            Interface.objects.create(name=instance.name + '_int_' + str(_),
                                     device=instance)
