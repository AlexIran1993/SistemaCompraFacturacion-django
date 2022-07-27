from django import forms
from .models import Categoria, Marca, Producto, SubCategoria, UnidadMedida
from inv import models

class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        #Campos del formualario
        fields = ['descripcion','estado']
        #Etiquetas de los campos
        labels = {
            'descripcion': "Descripcion de la categoria",
            'estado' : "Estado"
        }
        #Descripcion de elementos html que usaran los campos del formulario
        widget = {'descripcion': forms.TextInput}
    
    #Atributos y valores para los campos del formualrio
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SubCategoriaForm(forms.ModelForm):
    #Filtor los registros que se mostraran en el campo categoria
    categoria = forms.ModelChoiceField(
        #Los campos que traere seran los que en la propiedad estado sea True.
        queryset=Categoria.objects.filter(estado = True)
        .order_by('descripcion')
    )
    class Meta:
        model = SubCategoria
        fields = ['categoria', 'descripcion', 'estado']
        labels = {
            'descripcion': "Sub Categoria",
            'estado': "Estado"
        }
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['categoria'].empty_label = "Seleccione Categoria"

class MarcaForm(forms.ModelForm):
    class Meta:   
        model = Marca
        fields = ['descripcion', 'estado']
        labels = {'descripcion': "Descripcion de la Marca",
                "estado": "Estado" }
        widgets = {'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class UMForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['descripcion', 'estado']
        labels = {
            'descripcion': "Descripcion de la Unidad de Medida",
            "estado": "Estado"
        }
        widgets = {'descripcion': forms.TextInput()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 
            'codigo_barras', 
            'descripcion', 
            'estado', 
            'precio', 
            'existencia',
            'ultima_compra',
            'marca',
            'subcategoria',
            'unidad_medida',
            'foto'
        ]

        #Campos que estoy excluyendo del formulario
        excluide = ['um', 'fm', 'uc', 'fc']
        widgets = {'descripcion': forms.TextInput()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        #Atributos del formulario que no estaran habilitados para modificarse
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True
