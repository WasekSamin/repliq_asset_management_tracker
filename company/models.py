from django.db import models
from datetime import datetime


class Company(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(null=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-id", )

    def __str__(self):
        return str(self.id)
    
    # Get company object by pk
    def get_company_obj_by_pk(self, pk):
        try:
            company_obj = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None
        else:
            return company_obj
    

