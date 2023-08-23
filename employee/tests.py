from django.test import TestCase, Client
from .models import (
    Employee, Role
)
from company.models import (
    Company,
)
from django.urls import reverse


class TestCompanyViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.role_obj = Role.objects.create(
            title="Manager"
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

        # Role
        self.role_list_url = reverse("employee:role-list")
        self.role_detail_url = reverse("employee:role-detail", args=[self.role_obj.pk])

        # Employee
        self.emp_list_url = reverse("employee:employee-list")
        self.emp_detail_url = reverse("employee:employee-detail", args=[self.emp_obj.pk])

    ### Role
    def test_role_list_get(self):
        response = self.client.get(self.role_list_url)
        self.assertEquals(response.status_code, 200)

    def test_role_create_post(self):
        data = {"title": "Dummy role"}
        response = self.client.post(self.role_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_role_detail_get(self):
        response = self.client.get(self.role_detail_url)
        self.assertEquals(response.status_code, 200)

    def test_role_detail_put(self):
        data = {"title": "Dummy role updated"}
        response = self.client.put(self.role_detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_role_detail_delete(self):
        response = self.client.delete(self.role_detail_url, {"id": self.role_obj.pk}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_role_no_data_given_post(self):
        data = {}
        response = self.client.post(self.role_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_role_no_data_put(self):
        data = {}
        response = self.client.put(self.role_detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)


    ### Employee
    def test_employee_list_get(self):
        response = self.client.get(self.emp_list_url)
        self.assertEquals(response.status_code, 200)

    def test_employee_create_post(self):
        data = {"name": "Dummy employee", "email": "dummy@gmail.com", "company": self.company_obj.pk, "role": self.role_obj.pk}
        response = self.client.post(self.emp_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_employee_detail_get(self):
        response = self.client.get(self.emp_detail_url)
        self.assertEquals(response.status_code, 200)

    def test_employee_detail_put(self):
        data = {"name": "Dummy employee updated"}
        response = self.client.put(self.emp_detail_url, data, content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_employee_detail_delete(self):
        response = self.client.delete(self.emp_detail_url, {"id": self.emp_obj.pk}, content_type='application/json')
        self.assertEquals(response.status_code, 204)

    def test_employee_no_data_given_post(self):
        data = {}
        response = self.client.post(self.emp_list_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_employee_no_data_put(self):
        data = {}
        response = self.client.put(self.emp_detail_url, data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

