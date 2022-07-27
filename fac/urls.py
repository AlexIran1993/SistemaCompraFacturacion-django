from django.urls import path
from . import views, reportes

urlpatterns = [
    path('clientes/', views.ClienteView.as_view(), name="clientes_list"),
    path('clientes/new', views.ClienteNew.as_view(), name="cliente_new"),
    path('clientes/edit/<int:pk>', views.ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>', views.clienteInactivar, name="cliente_inactivar"),

    #Paths para las vistas de facturacion
    path('facturas/', views.FacturaView.as_view(), name="factura_list"),
    path('facturas/new', views.facturas, name="facturas_new"),
    path('facturas/buscar-producto', views.ProductoView.as_view(), name="factura_producto"),
    path('facturas/edit/<int:id>',views.facturas, name="factura_edit"),
    path('facturas/borrar-detalle/<int:id>',views.borrar_detalle_factura, name="factura_borrar_detalle"),
    path('facturas/imprimr/<int:id>', reportes.imprimir_factura_recibo, name="factura_imprimir_one"),
    path('facturas/imprimir-todas/<str:f1>/<str:f2>', reportes.imprimr_factura_list, name="factura_imprimir_all"),

    path('facturas/clientes/new/', views.cliente_add_modify, name="fac_cliente_add"),
    path('facturas/clientes/<int:pk>', views.cliente_add_modify, name="fac_cliente_mod")

]