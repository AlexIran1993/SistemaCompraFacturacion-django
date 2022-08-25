"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Direccion para el acceso a administraccion de Django
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secureloginfac/', admin.site.urls),
    #Path para el acceso a el archivo urls.py de la aplicacion bases
    path('', include(('bases.urls', 'bases'), namespace='bases')),
    #Path para el acceso a el archivo urls.py de la aplicacion inv
    path('inv/', include(('inv.urls', 'inv'), namespace='inv')),
    #Path para el acceso a el archivo urls.py de la aplicacion cmp
    path('cmp/', include(('cmp.urls', 'cmp'), namespace='cmp')),
    #Path para el acceso a el archivo urls.py de la aplicacion fac
    path('fac/', include(('fac.urls', 'fac'), namespace='fac')),
    #Path para el acceso del archivo urls.py de la aplicacion api
    path('api/', include(('api.urls', 'api'), namespace='api')),
]

#Configuracion de la locacion de las imagenes para que se puedan mostrar
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
