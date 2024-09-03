
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]
if settings.DEBUG == True:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)