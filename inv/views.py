from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Categoria, Marca, Producto, SubCategoria, UnidadMedida
from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UMForm, ProductoForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from bases.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
# Create your views here.

#Vistas para el manejo de los registros de las Categorias
class CategoriaView(SinPrivilegios ,generic.ListView):
    #Especificacion del modelo y template de referencia
    model = Categoria
    #Definicion del permiso requerido para visualizar el template categoria_list.html
    permission_required = "inv.view_categoria"
    template_name = 'inv/categoria_lis.html'
    context_object_name = 'obj'



#Clase que registra una nueva categoria 
class CategoriaNew(SuccessMessageMixin, SinPrivilegios ,generic.CreateView):
    #Definicion del permiso requerido para crear un nuevo registro en categoria
    permission_required = "inv.add_categoria"
    #Modelo tomado en cuenta
    model = Categoria
    #Plantilla donde se mostrara el formulario
    template_name = 'inv/categoria_form.html'
    #Objeto que se enviaria al template (opcional)
    context_object_name = 'obj'
    #Formulario con los campos a mostrar
    form_class = CategoriaForm
    #Redireccionamiento una vez que se haga el nuevo registro
    success_url = reverse_lazy("inv:categoria_list")
    #Mensaje que se enviara al template
    success_message = "Categoria Creada Satisfactoriamente"

    #Campo uc que se modificara con la data del usuario en sesion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

#Clase que editara la data de una categoria
class CategoriaEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    #Definicion del permiso requerido para actualizar un registro en categoria
    permission_required = "inv.change_categoria"
    #Modelo tomado en cuenta
    model = Categoria
    #Plantilla donde se mostrara el formulario
    template_name = 'inv/categoria_form.html'
    #Objeto que se enviaria al template (opcional)
    context_object_name = 'obj'
    #Formulario con los campos a mostrar
    form_class = CategoriaForm
    #Redireccionamiento una vez que se haga el nuevo registro
    success_url = reverse_lazy("inv:categoria_list")
    #Mensaje que se enviara al template
    success_message = "Categoria Actualizada Satisfactoriamente"

    #Campo uc que se modificara con la data del usuario en sesion
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('inv.change_categoria', login_url='bases:sin_privilegios')
def categoria_inactivar(request, id):
    categoria = Categoria.objects.filter(pk=id).first()

    if request.method == "POST":
        if categoria:
            categoria.estado = not categoria.estado
            categoria.save()
            return HttpResponse("OK")
        
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

@login_required(login_url="/login/")
@permission_required('inv.change_subcategoria', login_url='bases:sin_privilegios')
#Vistas para el manejo de los registros de las subcategorias
def subcategoria_inactivar(request,id):
    #Consulta a la base de datos
    subcategoria = SubCategoria.objects.filter(pk=id).first()

    if request.method == "POST":
        if subcategoria:
            subcategoria.estado = not subcategoria.estado
            subcategoria.save()
            return HttpResponse("OK")
        
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

class SubCategoriaView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_subcategoria"
    model = SubCategoria
    template_name='inv/subcategoria_list.html'
    context_object_name = 'obj'

    def get_queryset(self):
        qs = SubCategoria.objects.all()
        category_id = self.request.GET.get("lang")

        if category_id:
            qs = qs.filter(categoria__id=category_id)

        return qs

class SubCategoriaNew(SinPrivilegios, generic.CreateView):
    permission_required = "inv.add_subcategoria"
    model = SubCategoria,
    template_name = 'inv/subcategoria_form.html'
    context_object_name = 'obj'
    form_class = SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")

    #Campo uc que se modificara con la data del usuario en sesion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

#Clase que editara la data de una categoria
class SubCategoriaEdit(SinPrivilegios, generic.UpdateView):
    permission_required = "inv.change_subcategoria"
    #Modelo tomado en cuenta
    model = SubCategoria
    #Plantilla donde se mostrara el formulario
    template_name = 'inv/subcategoria_form.html'
    #Objeto que se enviaria al template (opcional)
    context_object_name = 'obj'
    #Formulario con los campos a mostrar
    form_class = SubCategoriaForm
    #Redireccionamiento una vez que se haga el nuevo registro
    success_url = reverse_lazy("inv:subcategoria_list")

    #Campo uc que se modificara con la data del usuario en sesion
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

#Vistas para el manejo de los registros de las marcas
class MarcaView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_marca"
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"

class MarcaNew(SinPrivilegios, generic.CreateView):
    permission_required = "inv.add_subcategoria"
    permission_required = "inv.add_marca"
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy('inv:marca_list')

    #Campo uc que se modificara con la data del usuario en sesion
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def marca_inactivar(request,id):
    #Consulta a la base de datos
    marca = Marca.objects.filter(pk=id).first()

    if request.method == "POST":
        if marca:
            marca.estado = not marca.estado
            marca.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

class MarcaEdit(SinPrivilegios, generic.UpdateView):
    permission_required = "inv.change_subcategoria"
    model = Marca
    template_name = 'inv/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marca_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class UMEdit(SinPrivilegios, generic.UpdateView):
    permission_required = "inv.change_unidadmedida"
    model = UnidadMedida
    template_name = "inv/um_form.html"
    context_object_name = 'obj'
    form_class = UMForm
    success_url = reverse_lazy("inv:um_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


#Vistas para el manejo de los registros de las Unidades de medida
class UMView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_unidadmedida"
    model = UnidadMedida
    template_name = 'inv/um_list.html'
    context_object_name = "obj"

class UMNew(SinPrivilegios, generic.CreateView):
    permission_required = "inv.add_unidadmedida"
    model = UnidadMedida
    template_name = "inv/um_form.html"
    context_object_name = 'obj'
    form_class = UMForm
    success_url = reverse_lazy("inv:um_list")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)

#Vistas para el manejor de los registros de Producto
class ProductoView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_producto"
    model = Producto
    template_name = 'inv/producto_list.html'
    context_object_name = "obj"

    def get_queryset(self):
        qs = Producto.objects.all()
        prod_desc = self.request.GET.get("lang")
        print(prod_desc)
        if prod_desc:
            print(qs)
            qs = qs.filter(subcategoria__descripcion=prod_desc)
            print(qs)
            if not qs:
                qs = Producto.objects.all()
                qs = qs.filter(marca__descripcion=prod_desc)
                print(qs)
                if not qs:
                    qs = Producto.objects.all()
                    qs = qs.filter(unidad_medida__descripcion=prod_desc)
                    print(qs)
        return qs

class ProductoNew(SuccessMessageMixin,SinPrivilegios,generic.CreateView):
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    success_message="Producto Creado"
    permission_required="inv.add_producto"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ProductoNew, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        return context



class ProductoEdit(SinPrivilegios, generic.UpdateView):
    permission_required = "inv.change_producto"
    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy("inv:producto_list")

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        #Obtencion del pk del registro que se editara
        pk = self.kwargs.get('pk')

        context = super(ProductoEdit, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()

        #Filtracion del regstro que se ubicara por el id
        context["obj"] = Producto.objects.filter(pk = pk).first()
        return context

@login_required(login_url="/login/")
@permission_required('inv.change_unidadmedida', login_url='bases:sin_privilegios')
def um_inactivar(request,id):
    um = UnidadMedida.objects.filter(pk=id).first()

    if request.method == "POST":
        if um:
            um.estado = not um.estado
            um.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")


@login_required(login_url="/login/")
@permission_required('inv.change_producto', login_url='bases:sin_privilegios')
def producto_inactivar(request,id):
    prod = Producto.objects.filter(pk=id).first()

    if request.method == "POST":
        if prod:
            prod.estado = not prod.estado
            prod.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")