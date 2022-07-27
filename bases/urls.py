from re import template
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
#Importacion de la vista Home
from bases.views import Home, HomeSinPrivilegios, IdiomaList, FraseList

urlpatterns = [
    path('', Home.as_view(), name='home' ),
    #Path para el login del usuario
    path('login/', auth_views.LoginView.as_view(template_name = 'base/login.html'), name='login'),
    #Path para el logout del usuario
    path('logout/', auth_views.LogoutView.as_view(template_name='bases/login.html'), name='logout'),
    #Path que mostrara el template sin privilegios.
    path('sin_privilegios/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),

    path('idiomas/', IdiomaList.as_view(), name="idiomas"),
    path('frase/', FraseList.as_view(), name="frases"),
]