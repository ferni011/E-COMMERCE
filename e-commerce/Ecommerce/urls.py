from django.contrib import admin
from django.urls import path,include
from etienda import views
from etienda.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('etienda/', include('etienda.urls')),
    path('', views.Home.as_view(), name='home'),
    path("api/", api.urls),
]
