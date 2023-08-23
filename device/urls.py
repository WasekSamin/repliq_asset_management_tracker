from django.urls import path

from .views import (
    CategoryList, CategoryDetail,
    DeviceList, DeviceDetail,
    DeviceDistributionList, DeviceDistributionDetail
)

app_name = "device"
urlpatterns = [
    # Category
    path("category/list/", CategoryList.as_view(), name="category-list"),
    path("category/detail/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    # Device
    path("list/", DeviceList.as_view(), name="device-list"),
    path("detail/<int:pk>/", DeviceDetail.as_view(), name="device-detail"),
    # Device Distribution
    path("distribution/list/", DeviceDistributionList.as_view(), name="device-distribution-list"),
    path("distribution/detail/<int:pk>/", DeviceDistributionDetail.as_view(), name="device-distribution-detail"),
]