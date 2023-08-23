from django.urls import path

from .views import (
    RoleList, RoleDetail,
    EmployeeList, EmployeeDetail
)

app_name = "employee"
urlpatterns = [
    # Role
    path("role/list/", RoleList.as_view(), name="role-list"),
    path("role/detail/<int:pk>/", RoleDetail.as_view(), name="role-detail"),
    # Employee
    path("list/", EmployeeList.as_view(), name="employee-list"),
    path("detail/<int:pk>/", EmployeeDetail.as_view(), name="employee-detail"),
]