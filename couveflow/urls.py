from django.contrib import admin
from django.urls import path

from couveflow.core.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    *urlpatterns,
]
