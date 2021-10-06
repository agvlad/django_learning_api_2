from django.contrib import admin
from .models import Hardware, Interface, Device, Network

admin.site.register(Hardware)
admin.site.register(Interface)
admin.site.register(Device)
admin.site.register(Network)
