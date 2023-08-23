from django.test import TestCase, Client
from .models import (
    Category, Device, DeviceDistribution
)
from employee.models import (
    Employee,
)
from company.models import (
    Company,
)
from django.urls import reverse
from datetime import datetime


class TestCompanyViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.cat_obj = Category.objects.create(
            title="Test category"
        )
        self.device_obj = Device.objects.create(
            name="Laptop",
            device_category=self.cat_obj,
            device_condition="new"
        )
        self.company_obj = Company.objects.create(
            name="Test company",
            email="company@gmail.com"
        )
        self.emp_obj = Employee.objects.create(
            name="Test employee",
            email="test@gmail.com",
            company=self.company_obj
        )
        self.dev_dist_obj = DeviceDistribution.objects.create(
            employee=self.emp_obj,
            returned_at=datetime.now(),
            returned_condition="ok"
        )
        self.dev_dist_obj.devices.add(self.device_obj.id)

        # Category
        self.cat_list_url = reverse("device:category-list")
        self.cat_detail_url = reverse("device:category-detail", args=[self.cat_obj.pk])

        # Device
        self.device_list_url = reverse("device:device-list")
        self.device_detail_url = reverse("device:device-detail", args=[self.device_obj.pk])

        # Device distribution
        self.dev_dist_list_url = reverse("device:device-distribution-list")
        self.dev_dist_detail_url = reverse("device:device-distribution-detail", args=[self.dev_dist_obj.pk])

    ### Category
    def test_category_list_get(self):
        response = self.client.get(self.cat_list_url)
        self.assertEquals(response.status_code, 200)

    def test_category_create_post(self):
        data = {"title": "Dummy category"}
        response = self.client.post(self.cat_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_category_detail_get(self):
        response = self.client.get(self.cat_detail_url)
        self.assertEquals(response.status_code, 200)

    def test_category_detail_put(self):
        data = {"title": "Dummy category updated"}
        response = self.client.put(self.cat_detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_category_detail_delete(self):
        response = self.client.delete(self.cat_detail_url, {"id": self.cat_obj.pk}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_category_no_data_given_post(self):
        data = {}
        response = self.client.post(self.cat_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_category_no_data_put(self):
        data = {}
        response = self.client.put(self.cat_detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)


    ### Device
    def test_device_list_get(self):
        response = self.client.get(self.device_list_url)
        self.assertEquals(response.status_code, 200)

    def test_device_create_post(self):
        data = {"name": "Dummy Device", "device_category": self.cat_obj.pk, "device_condition": "new"}
        response = self.client.post(self.device_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_device_detail_get(self):
        response = self.client.get(self.device_detail_url)
        self.assertEquals(response.status_code, 200)

    def test_device_detail_put(self):
        data = {"name": "Dummy device updated", "device_condition": "used"}
        response = self.client.put(self.device_detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_device_detail_delete(self):
        response = self.client.delete(self.device_detail_url, {"id": self.device_obj.id}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_device_no_data_given_post(self):
        data = {}
        response = self.client.post(self.device_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_device_no_data_put(self):
        data = {}
        response = self.client.put(self.device_detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)


    ### Device distribution
    def test_device_distribution_list_get(self):
        response = self.client.get(self.dev_dist_list_url)
        self.assertEquals(response.status_code, 200)

    def test_device_distribution_create_post(self):
        data = {"employee": self.emp_obj.pk, "devices": [self.device_obj.pk], "returned_at": datetime.now(), "returned_condition": "ok"}
        response = self.client.post(self.dev_dist_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_device_distribution_detail_get(self):
        response = self.client.get(self.dev_dist_detail_url)
        self.assertEquals(response.status_code, 200)

    def test_device_distribution_detail_put(self):
        data = {"returned_condition": "damaged"}
        response = self.client.put(self.dev_dist_detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_device_distribution_detail_delete(self):
        response = self.client.delete(self.dev_dist_detail_url, {"id": self.dev_dist_obj.pk}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_device_distribution_no_data_given_post(self):
        data = {}
        response = self.client.post(self.dev_dist_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_device_distribution_no_data_put(self):
        data = {}
        response = self.client.put(self.dev_dist_detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 200)

