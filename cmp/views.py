import datetime
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Sum

from inv.models import Producto
from .models import Proveedor, ComprasEnc, ComprasDet
from .forms import ProveedorForm, ComprasEncForm
from django.http import HttpResponse, JsonResponse
from bases.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class ProveedorView(SinPrivilegios, generic.ListView):
    permission_required = "cmp.view_proveedor"
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"

class Proveedornew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = "cmp.add_proveedor"
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    success_message = "Proveedor Nuevo"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)
    
class ProveedorEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    permission_required = "cmp.change_proveedor"
    model = Proveedor
    template_name = "cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("cmp:proveedor_list")
    success_message = "Proveedor Editado"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)

@login_required(login_url="/login/")
@permission_required('cmp.change_proveedor', login_url='bases:sin_privilegios')
def proveedor_inactivar(request, id):
    prv = Proveedor.objects.filter(id=id).first()
    if request.method == "POST":
        if prv:
            prv.estado = not prv.estado
            prv.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

class ComprasView(SinPrivilegios, generic.ListView):
    model = ComprasEnc
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    permission_required = "cmp.view_comprasenc"

@login_required(login_url="/login/")
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request, compra_id=None):
    #Filtrado de los registros de la tabla Producto.
    producto = Producto.objects.filter(estado = True)
    
    #Inicializacion de los objetos Json.
    form_compras={}
    contexto={}

    #Valido que el metodo dentro del request sea de tipo GET
    if request.method == 'GET':
        #Instanciamiento del formulario
        form_compras = ComprasEncForm()
        #Busco el encabezado de la compra filtrando por el id del parametro
        enc = ComprasEnc.objects.filter(pk = compra_id).first()

        #Valido que la busqueda del encabezado sea correcta
        if enc:
            #Busco el detalle del encabezado usandolo como filtro.
            det = ComprasDet.objects.filter(compra = enc)
            #Renderizado de fecha_compra y fecha_factura.
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)

            #Objeto Json con los valores para el formulario
            e = {
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }

            #Renderizado del formulario con los datos del objeto e
            form_compras = ComprasEncForm(e)

        else:
            det = None
        
        #Objeto Json con la data que se enviara al template
        contexto = {
            #Objeto del producto
            'producto': producto,
            #Objeto encabezedo del producto
            'encabezado': enc,
            #Objeto detalle del producto
            'detalle': det,
            #Objeto con el formulario del producto
            'form_enc': form_compras
        }
    
    if request.method == "POST":
        #Obtencion de la data del formulario
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")

        #Inicializacion de las variable enteras
        sub_total = 0
        descuento = 0
        total = 0

        #Evaluo el parametro compra_id, en caso de que sea nulo sera una señal de que el ecabezado no existe.
        if not compra_id:
            proveedor = Proveedor.objects.get(id = proveedor)

            #Objeto de tipo ComprasEnc
            enc = ComprasEnc(
                fecha_compra = fecha_compra,
                observacion = observacion,
                no_factura = no_factura,
                fecha_factura = fecha_factura,
                proveedor = proveedor,
                uc = request.user
            )

            #Valido que el objeto enc se haya creado con exito, en caso de que asi sea guardo el nuevo encabezado
            if enc:
                enc.save()
                compra_id = enc.id
        else:
            enc = ComprasEnc.objects.filter(pk = compra_id).first()
            
            #Actualizo la data del objeto enc.
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura = no_factura
                enc.fecha_factura = fecha_factura
                enc.um = request.user.id
                enc.save()

        if not compra_id:
            return redirect("cmp:compras_list")

        #Recaptura de los datos para el detalle
        producto = request.POST.get("id_id_producto")
        cantida = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle = request.POST.get("id_descuento_detalle")
        total_detalle = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk = producto)

        #Creacion del objeto de tipo comprasDet
        det = ComprasDet(
            compra = enc,
            producto = prod,
            cantidad = cantida,
            precio_prv = precio,
            descuento = descuento_detalle,
            costo = 0,
            uc = request.user
        )

        if det:
            det.save()

            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento=descuento["descuento__sum"]
            enc.save()

        return redirect("cmp:compras_edit", compra_id = compra_id)

    #Envio de datos al template
    return render(request, 'cmp/compras.html', contexto)

#Vista que eliminara un producto de la compra
class compraDetDelete(SinPrivilegios, generic.DeleteView):
    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'

    def get_success_url(self):
        #Obtengo el id del producto que se envia por la url y lo almaceno en una variable con el mismo nombre
        compra_id = self.kwargs['compra_id']
        #Se ejecuta un reverse_lazy al template compras_edit junto con un kwargs con el valor de compra_id
        return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})

@login_required(login_url="/login/")
@permission_required('cmp.change_comprasenc', login_url='bases:sin_privilegios')
def compra_inactivar(request,id):
    compra = ComprasEnc.objects.filter(id=id).first()
    if request.method == "POST":
        if compra:
            compra.estado = not compra.estado
            compra.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")
