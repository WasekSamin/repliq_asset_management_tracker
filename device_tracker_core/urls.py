from django.contrib import admin
from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Device Tracker API",
      default_version='v1',
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    path("api/company/", include("company.urls")),
    path("api/employee/", include("employee.urls")),
    path("api/device/", include("device.urls")),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
