from django.db import models
from bases.models import ClaseModelo
# Create your models here.

#Modelo Categoria
class Categoria(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la categoria',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    #Señalo que la propiedad descripcion se vizualice en mayusculas
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()

    #Nombramento del pluran en Django
    class Meta:
        verbose_name_plural = "Categorias"

class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la categoria',
    )

    def __str__(self):
        #El formato en el que se mostrara sera descripcion de la categoria/descripcion de la subcategoria
        return '{}:{}'.format(self.categoria.descripcion, self.descripcion)
    
    #Guardo el registro en mayusculas
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    #Nombramento del pluran en Django
    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'descripcion')

class Marca(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text= 'Descripcion de la Marca',
        unique= True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Marca, self).save()
    
    class Meta:
        verbose_name_plural = "Marcas"

class UnidadMedida(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la Unidad de Medida',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        try:
            super(UnidadMedida, self).save()
        except:
            pass
    
    class Meta:
        verbose_name_plural = "Unidades de Medida"

class Producto(ClaseModelo):
    #Atributos propios del modelo Producto
    codigo = models.CharField(max_length=20, unique= True)
    codigo_barras = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    existencia = models.IntegerField(default=0)
    ultima_compra = models.DateField(null = True, blank=True)

    #Llaves foraneas de los modelos.
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)

    #Propieda que almcenara una imagen del producto
    foto = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto, self).save()
    
    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('codigo', 'codigo_barras')