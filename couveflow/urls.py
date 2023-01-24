from django.contrib import admin
from django.urls import path

from couveflow.core.urls import router as core_router

urlpatterns = [
    path('admin/', admin.site.urls),
    *core_router.urls
]
