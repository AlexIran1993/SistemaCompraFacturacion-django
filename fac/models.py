from django.db import models
from bases.models import ClaseModelo, ClaseModelo2
from inv.models import Producto

#signals
#signal usado para vigilar un modelos despues de guardalo o elimnaralo
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum



#Modelo cliente
class Cliente(ClaseModelo):
    #Variables que se usaran para identificar a un cliente natural o juridico
    NAT = 'Natural'
    JUR = 'Juridica'
    TIPO_CLIENTE = [
        (NAT, 'Natural'),
        (JUR, 'Juridica')
    ]
    #Propiedades de la clase Cliente
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    celular = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CLIENTE, default=NAT)

    def __str__(self):
        return '{} {}'.format(self.apellido,self.nombre)
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Cliente, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Clientes"

#Modelo heredando la nueva ClaseModelo
class FacturaEnc(ClaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{} {}'.format(self.id, self.cliente)
    
    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc, self).save()
    
    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name = "Encabezado Factura"
        #Permiso Personalizado
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
        ]

class FacturaDet(ClaseModelo2):
    factura = models.ForeignKey(FacturaEnc, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)
    
    def save(self):
        self.sub_total = float(float(int(self.cantidad))) * float(self.precio)
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()

    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name = "Detalle Factura"
                #Permiso Personalizado
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]

#Funcion que altera el sub_total y total de FacturaEnc
@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender, instance, **kwargs):
    #Extraigo el id d la factura y el id del producto que se encuentra en el objeto que se regsitrara en la tabla FacturaEnc
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    #Traigo el regsitro de FacturaEnc que coincida con el id de la variable factura_id
    enc = FacturaEnc.objects.get(pk = factura_id)
    if enc:
        #Busco el registro de FacturaDet que coincida con el valor de factura_id y le extraigo el valor de sub_total
        sub_total = FacturaDet.objects.filter(factura=factura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total', 0.00)
        #Busco el registro de FacturaDet que coincida con el valor de factura_id y le extraigo el valor de descuento
        descuento = FacturaDet.objects.filter(factura=factura_id).aggregate(descuento=Sum('descuento')).get('descuento', 0.00)

        #Actualizacion de los datos de FacturaEnc
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()
    
    #Inicializacion de los productos
    prod = Producto.objects.filter(pk=producto_id).first()
    if prod:
        #Actualizacino de la propiedad cantidad 
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()