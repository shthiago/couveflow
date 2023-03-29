from django.conf import settings
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from rest_framework.authtoken import views

from couveflow.core.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('graphql/', GraphQLView.as_view(graphiql=settings.DEBUG)),
    *urlpatterns,
]
