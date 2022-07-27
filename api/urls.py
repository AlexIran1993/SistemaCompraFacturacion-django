from django.urls import path, include
from . import views

urlpatterns = [
    path('v1/productos/', views.ProductoList.as_view(),name='producto_list'),
    path('v1/producto/<str:codigo>', views.ProductoDetalle.as_view(), name='producto_detalle'),

    path('v1/clientes/', views.ClienteList.as_view(), name='cliente_list')
]