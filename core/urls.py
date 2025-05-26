from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from apps.users.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('djoser.urls')),                            
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/jwt/logout/', LogoutView.as_view(), name='jwt_logout'),

    # Схема OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (опционально)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]


if not settings.PROD:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)