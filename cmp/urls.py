from django.urls import path, include
from . import views

#Importacion de la vista reporte_compras
from . import reportes

urlpatterns = [
    #Rutas para la seccion de proveedores
    path('proveedores/', views.ProveedorView.as_view(), name="proveedor_list"),
    path('proveedor/new', views.Proveedornew.as_view(), name="proveedor_new"),
    path('proveedor/edit/<int:pk>', views.ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedor/inactivar/<int:id>', views.proveedor_inactivar, name="proveedor_inactivar"),

    #Rutas para la seccion de Compras
    path('compras/', views.ComprasView.as_view(), name="compras_list"),
    path('compras/new', views.compras, name="compras_new"),
    path('compras/edit/<int:compra_id>', views.compras, name="compras_edit"),
    path('compras/<int:compra_id>/delete/<int:pk>', views.compraDetDelete.as_view(), name="compras_del"),
    path('compras/inactivar/<int:id>', views.compra_inactivar, name="compra_inactivar"),

    #Rutas para la creacion de archivos pdf
    path('compras/listado', reportes.reporte_compras, name='compras_print_all'),
    path('compras/<int:compra_id>', reportes.imprimir_compra, name="compra_print_one"),
]
