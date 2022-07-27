from django.contrib import admin
from .models import Proveedor, ComprasEnc, ComprasDet
# Register your models here.

admin.site.register(Proveedor)
admin.site.register(ComprasEnc)
admin.site.register(ComprasDet)