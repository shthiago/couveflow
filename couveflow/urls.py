from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

from couveflow.core.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    *urlpatterns,
]
