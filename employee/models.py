from django.db import models
from company.models import Company
from datetime import datetime


# Employee roles
class Role(models.Model):
    title = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return self.title
    
    # Get role object by pk
    def get_role_obj_by_pk(self, pk):
        try:
            role_obj = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None
        else:
            return role_obj


class Employee(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return str(self.id)
    
    # Get employee object using pk
    def get_employee_obj_by_pk(self, pk):
        try:
            emp_obj = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None
        else:
            return emp_obj

