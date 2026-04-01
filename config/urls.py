from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),

    # OpenAPI Schema generation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI and ReDoc
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
