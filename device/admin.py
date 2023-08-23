from django.contrib import admin

from .models import (
    Category, Device, DeviceDistribution
)

admin.site.register(Category)
admin.site.register(Device)
admin.site.register(DeviceDistribution)