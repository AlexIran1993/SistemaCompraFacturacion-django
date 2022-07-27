from django.urls import path
from . import views
urlpatterns = [
    #paths para el manejo de categorias
    path('categorias/', views.CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new', views.CategoriaNew.as_view(), name='categoria_new'),
    path('categoria/edit/<int:pk>', views.CategoriaEdit.as_view(), name='categoria_edit'),
    path('categoria/inactivar/<int:id>', views.categoria_inactivar, name="categoria_inactivar"),

    #Paths para el manejo de subcategorias
    path('subcategorias/', views.SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new', views.SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>', views.SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategoria/inactivar/<int:id>', views.subcategoria_inactivar, name="subcategoria_inactivar"),


    #Paths para el manejo de marcas
    path('marcas/', views.MarcaView.as_view(), name='marca_list'),
    path('marcas/new/', views.MarcaNew.as_view(), name="marca_new"),
    path('marcas/edit/<int:pk>', views.MarcaEdit.as_view(), name="marca_edit"),
    path('marcas/inactivar/<int:id>', views.marca_inactivar, name="marca_inactivar"),

    #Paths para el manejo de las unidades de medida
    path('um/', views.UMView.as_view(), name='um_list'),
    path('um/new/', views.UMNew.as_view(), name="um_new"),
    path('um/edit/<int:pk>', views.UMEdit.as_view(), name="um_edit"),
    path('um/inactivar/<int:id>', views.um_inactivar, name="um_inactivar"),

    #Pathas para el manejo de los Productos
    path('productos/', views.ProductoView.as_view(), name="producto_list"),
    path('producto/new/', views.ProductoNew.as_view(), name='producto_new'),
    path('producto/edit/<int:pk>', views.ProductoEdit.as_view(), name='producto_edit'),
    path('producto/inactivar/<int:id>', views.producto_inactivar, name='producto_inactivar'),
]