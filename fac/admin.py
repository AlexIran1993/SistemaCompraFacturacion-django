from django.contrib import admin
from .models import Cliente, FacturaDet, FacturaEnc
# Register your models here.

class FacturaEncAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'fecha',
        'sub_total',
        'descuento',
        'total',
        'estado',
        'fc',
        'fm'
    )

class FacturaDetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'factura',
        'producto',
        'cantidad',
        'precio',
        'sub_total',
        'descuento',
        'total',
        'fc',
        'fm'

    )

admin.site.register(Cliente)
admin.site.register(FacturaEnc, FacturaEncAdmin)
admin.site.register(FacturaDet, FacturaDetAdmin)