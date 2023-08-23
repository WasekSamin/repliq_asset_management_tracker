from django.urls import path

from .views import (
    CompanyList, CompanyDetail, CompanyDeviceCheckView,
)

app_name = "company"
urlpatterns = [
    path("list/", CompanyList.as_view(), name="company-list"),
    path("detail/<int:pk>/", CompanyDetail.as_view(), name="company-detail"),
    path("device-check/<int:company_pk>/", CompanyDeviceCheckView.as_view(), name="company-device-check"),
]