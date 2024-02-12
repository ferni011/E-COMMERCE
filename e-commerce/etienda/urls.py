from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultaelectronica/', views.consultaElectronica, name='cons-elec'),
    path('consultadescripcion/', views.consultaDescripcion, name='cons-desc'),
    path('consultapuntuacion/', views.consultaPuntuacion, name='cons-punt'),
    path('consultahombrepuntuacion/', views.consultaHombrePuntuacion, name='cons-homb-punt'),
    path('consultafacturaciontotal/', views.consultaFacturacion, name='cons-fact-total'),
    path('consultafacturacioncategorias/', views.consultaFacturacionCategorias, name='cons-fact-categoria'),
    path('landing-page/', views.landingPage , name="landingPage"),
    path('categoria/<slug:cat_prod>/', views.categoriaProducto , name="categoriaProducto"),
    path('busqueda/', views.busquedaPalabra, name="busquedaProducto"),
    path('anadir/', views.anadirProducto, name="anadir-producto"),
]

