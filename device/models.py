from django.db import models
from datetime import datetime
from employee.models import Employee

# Create your models here.

# Device category -> mobile, laptop etc.
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return self.title
    
    # Get category object using pk
    def get_category_obj_by_pk(self, pk):
        try:
            cat_obj = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None
        else:
            return cat_obj


DEVICE_CONDITION = (
    ("used", "used"),
    ("new", "new")
)

class Device(models.Model):
    name = models.CharField(max_length=120)
    device_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    device_condition = models.CharField(max_length=120, null=True, blank=True, choices=DEVICE_CONDITION)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return str(self.id)
    
    # Get device object using pk
    def get_device_obj_by_pk(self, pk):
        try:
            device_obj = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return None
        else:
            return device_obj
    

DEVICE_RETURN_CONDITION = (
    ("ok", "ok"),
    ("damaged", "damaged")
)

class DeviceDistribution(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    devices = models.ManyToManyField(Device) # One or more devices can be distributed to one employee
    checkout_at = models.DateTimeField(default=datetime.now)
    returned_at = models.DateTimeField(null=True, blank=True)
    returned_condition = models.CharField(max_length=120, choices=DEVICE_RETURN_CONDITION, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return str(self.id)