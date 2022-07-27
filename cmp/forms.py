from socket import fromshare
from django import forms
from .models import Proveedor, ComprasEnc

class ProveedorForm(forms.ModelForm):
    #Especifico que el textinput de email devera estar estructurado como un email.
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Proveedor
        exclude = ['um','fm','uc','fc']
        widget = {'descripcion': forms.TextInput()}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
    
    def clean(self):
        try:
            #Busqueda del regsitro que concida con el nuevo que esta en el formualrio
            sc = Proveedor.objects.get(
                descripcion = self.cleaned_data["descripcion"].upper()
            )
            #Validacion de que el pk del nuevo registro sea nullo, en caso de ser asi, es señal de que se intenta crear un nuevo registro con la misma descripcion
            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            #Se valida que el pk del formulario sea diferente al pk de registro que se trajo de la base de datos, de ser asi es señal de que se intenta actualizar un registro con la descripcion de otro.
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")

        #En caso de que el regsitro no se encuentre, sera señal de que el nuevo registro es nuevo 
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data

class ComprasEncForm(forms.ModelForm):
    #Campos del formulario
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model = ComprasEnc
        fields = [
            'proveedor', 'fecha_compra', 'observacion',
            'no_factura', 'fecha_factura', 'sub_total',
            'descuento', 'total'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        #Campos de solo lectura
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
