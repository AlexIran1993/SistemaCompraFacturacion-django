from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
# Create your models here.

#Clase modelo general
class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    #Fecha de creacion
    fc = models.DateField(auto_now_add=True)
    #Fecha de modificacion
    fm = models.DateField(auto_now=True)
    #Objeto foreingkey del usuario
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    #Unidad de medida
    um = models.IntegerField(blank=True, null=True)

    #Señalizacion para que Django no tome en cuneta a la clase CalseModelo para la migracion
    class Meta:
        abstract = True

class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    #Fecha de creacion
    fc = models.DateField(auto_now_add=True)
    #Fecha de modificacion
    fm = models.DateField(auto_now=True)

    #Objeto foreingkey del usuario
    #uc = models.ForeignKey(User, on_delete=models.CASCADE)
    #Unidad de medida
    #um = models.IntegerField(blank=True, null=True)

    uc = UserForeignKey(auto_user_add = True, related_name = '+')
    um = UserForeignKey(auto_user = True, related_name = '+')

    #Señalizacion para que Django no tome en cuneta a la clase CalseModelo para la migracion
    class Meta:
        abstract = True

class Idioma(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.nombre

class Frase(models.Model):
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    autor = models.CharField(max_length=50, default="Anonimo")
    frase = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Frases"

    def __str__(self):
        return "{} - {}".format(self.autor,self.idioma)
