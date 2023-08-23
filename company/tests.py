from django.test import TestCase, Client
from .models import Company
from django.urls import reverse


class TestCompanyViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.company_obj = Company.objects.create(
            name="Test company",
            email="test@gmail.com"
        )

        self.list_url = reverse("company:company-list")
        self.detail_url = reverse("company:company-detail", args=[self.company_obj.pk])
        self.device_check_url = reverse("company:company-device-check", args=[self.company_obj.pk])

    def test_company_list_get(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)

    def test_company_create_post(self):
        data = {"name": "Dummy", "email": "dummy@gmail.com"}
        response = self.client.post(self.list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_company_detail_get(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)

    def test_company_detail_put(self):
        data = {"name": "Test 2"}
        response = self.client.put(self.detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_company_detail_delete(self):
        response = self.client.delete(self.detail_url, {"id": self.company_obj.pk}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_company_no_data_given_post(self):
        data = {}
        response = self.client.post(self.list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_company_no_data_put(self):
        data = {}
        response = self.client.put(self.detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_company_device_check_get(self):
        response = self.client.get(self.device_check_url)
        self.assertEquals(response.status_code, 200)

