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
from apps.users.views import ActivationGetView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/map/', include('apps.map.urls')),
    path('api/v1/order/', include('apps.order.urls')),

    path('api/auth/', include('djoser.urls')),                            
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/jwt/logout/', LogoutView.as_view(), name='jwt_logout'),

    # Схема OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (опционально)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path(
        'api/auth/activate/<str:uid>/<str:token>/',
        ActivationGetView.as_view(),
        name='user-activation'
    ),

]


if not settings.PROD:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)