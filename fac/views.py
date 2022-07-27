from operator import inv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from platformdirs import user_cache_dir
from .models import Cliente, FacturaDet, FacturaEnc
from bases.views import SinPrivilegios
from django.views import generic
from .forms import ClienteForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
import inv.views as inv
from django.contrib import messages
from inv.models import Producto
from django.contrib.auth import authenticate

# Vistas para el manejo de clienyes
class ClienteView(SinPrivilegios, generic.ListView):
    permission_required = "fac.view_cliente"
    model = Cliente
    template_name = "fac/clientes_list.html"
    context_object_name = "obj"

class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    context_object_name = 'obj'
    success_message  ="Registro Agregado Satisfatoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    context_object_name = 'obj'
    success_message = "Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class ClienteNew(VistaBaseCreate):
    model = Cliente
    template_name = "fac/cliente_form.html"
    form_class = ClienteForm
    success_url = reverse_lazy("fac:clientes_list")
    permission_required = "fac.add_cliente"

    #Metodo que evaluara el redijimiento del template sobreescribiendo el metodo get para obtener el querystring
    def get(self, request, *args, **kwargs):
        print("sobre escribir get")

        #Obtencion del queryset evaluando que exista el valor "t" dentro del request.GET.
        try:
            t = request.GET["t"]
        except:
            #En caso de que no se encuntre el valor, igualo a none el objeto t.
            t = None
        
        print(t)
        #Inicializacion del formulario
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})

class ClienteEdit(VistaBaseEdit):
        model = Cliente
        template_name = "fac/cliente_form.html"
        form_class = ClienteForm
        success_url = reverse_lazy("fac:clientes_list")
        permission_required = "fac.change_cliente"

        def get(self, request, *args, **kwargs):
            print("sobre escribir get en edit")

            #print(request)

            #Obtencion del querystring
            try:
                t = request.GET["t"]
            except:
                t = None
            
            print(t)
            #Inicializacion del objeto con la data que llega como parametro
            self.object = self.get_object()
            #Obtencion del fomrualrio segun la definicion de la clase
            form_class = self.get_form_class()
            #Inicializacion del formualrio
            form = self.get_form(form_class)
            #Creacion del objeto context con la data del objeto, la inicializacion del formulario y el querysrtring
            context = self.get_context_data(object=self.object, form=form,t=t)
            #print(form_class,form,context)
            #Return al formulario con la data del context
            return self.render_to_response(context)

@login_required(login_url="/login/")
@permission_required("fac.change_cliente", login_url="/login/")
def clienteInactivar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method == "POST":
        if cliente:
            #Cambio el valor de la propiedad estado a su valor invserso (de true a false o false a true)
            cliente.estado = not cliente.estado
            cliente.save()
            #Respuesta de retorno para la accion success en Frontend.
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")


#Vistas para el manejo de las facturas
class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required = "fac.view_facturaenc"

    #Metodo que filtrara la lista de facturas segun el usuario en sesion
    def get_queryset(self):
        #Obtencion de la data del usuario en sesion
        user = self.request.user
        #print(user)
        #Consulta que se ejecutara, por lo pronto sea una ejeucion de si misma para traer todas las facturas
        qs = super().get_queryset()
        #Recorrido de qs para ver las facturas creadas por el usuario
        for q in qs:
            #Imprecion del usuario que cre el registro y id del registro.
            print(q.uc, q.id)

        #Valido si el usuario no es superuser.
        if not user.is_superuser:
            #Filtro los registros que coincidan la pripiedad user con la columna uc.
            qs = qs.filter(uc=user)

        #Recorro nuevamnte la lista de registro ya con el filtro aplicado.
        for q in qs:
            print(q.uc,q.id)
        return qs
        

@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request, id=None):
    template_name='fac/facturas.html'
    detalle = {}

    #Busqueda de los clientes cuando la propieda estado es True
    clientes = Cliente.objects.filter(estado=True)

    #Validacion del metodo en el request
    if request.method == "GET":
        #Busqueda de la factura segun el parametero id
        enc = FacturaEnc.objects.filter(pk=id).first()

        #Evaluo que el parametro id no sea nulo
        if id:
            #Evaluo que la factura que se pretende editar exista en la base de datos
            if not enc:
                messages.error(request, 'La factura que se pretende editar no existe')
                return redirect("fac:factura_list")
            #Extraigo la data del usuario en sesion y lo almaceno en una variable
            usr = request.user
            #Evaluo que el usuario en sesion no sea sueperuser
            if not usr.is_superuser:
                #Evaluo que la propiedad uc sea igual a usr, en caso de que no lo sea no puede editar este registro
                if enc.uc != usr:
                    messages.error(request, "Esta Factura no puede ser editada por ti")
                    return redirect("fac:factura_list")
            

        #Si el objeto enc esta vacio se crea el objeo encabezado con valores iniciales
        if not enc:
            encabezado = {
                'id': 0,
                'fecha': datetime.today(),
                'cliente': 0,
                'sub_total': 0.00,
                'descuento': 0.00,
                'total': 0.00
            }
            #Creacion del obejto detalle como None ya que no existe factura para este cliente
            detalle = None
        #Si el objeto enc no esta vacio, creo un objeto encabezado con los valores de enc
        else:
            encabezado = {
                'id': enc.id,
                'fecha': enc.fecha,
                'cliente': enc.cliente,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            #Busco el detallado de esa factura
            detalle = FacturaDet.objects.filter(factura=enc)
            
        #Objeto de Retorno para el template
        contexto = {
            "enc": encabezado,
            "det": detalle,
            "cliente": clientes
        }
        return render(request, template_name, contexto)

    #Creacion de la factura con datos del formulario del template facturas.html
    if request.method == "POST":
        #Almacenamiento de los datos procedentes del formulario
        cliente = request.POST.get("enc_cliente")
        fecha = request.POST.get("fecha")
        
        #Extraigo el registro del cliente de la base de datos
        clie = Cliente.objects.get(pk = cliente)

        #Si el parametro id esta vacio, es señal de que la factura es nueva.
        if not id:
            enc = FacturaEnc(
                cliente = clie,
                fecha = fecha
            )
            #Si el objeto enc es correcto, guardo el nuevo registro en la base de datos y extraigo el id de ese registro
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = clie
                enc.save()
        
        if not id:
            messages.error(request, "No Es Posible Detectar No. De Factura")
            return redirect("fac:facturas_list")
        
        #Agregado del detallado de la factura
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        prod = Producto.objects.get(codigo = codigo)

        det = FacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            descuento = descuento,
            total = total
        )
        if det:
            det.save()
        
        return redirect("fac:factura_edit", id=id)
    return render(request, template_name, contexto)

class ProductoView(inv.ProductoView):
    template_name = "fac/buscar_producto.html"

def borrar_detalle_factura(request, id):
    template_name = "fac/factura_borrar_detalle.html"
    det = FacturaDet.objects.get(pk=id)

    if request.method == "GET":
        contexto = {
            "det": det
        }
    
    if request.method == "POST":
        #Extraccin de la data del usuario que se envio por el request.POST
        usuario = request.POST.get("usuario")
        pas = request.POST.get("pass")

        #Autenticacion del usuario que se extrajo del metodo POST
        user =authenticate(username=usuario,password=pas)

        #Validacion que el objeto user no sea None o que este activo en la base de datos
        if not user:
            return HttpResponse("Usuario o Clave incorrecta")
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        #Validacin que el objeto user contenga un superusuario o tenga el permiso para actualiza los registros de FacturaDet
        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            #Hago un clonado del objeto det
            det.id = None
            #Niego los valores que se creareon en la clonacion del det original
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")
        
        return HttpResponse("Usuario no autorizado")


    return render(request, template_name, contexto)

@login_required(login_url="/login/")
@permission_required("fac.change_cliente", login_url="/login/")
def cliente_add_modify(request, pk=None):
    #Definicion del template donde se retornara
    template_name = "fac/cliente_form.html"
    #Objeto Json con la data que se usara en el template
    context = {}

    #Validacion del tipo de metodo en el request
    if request.method == "GET":
        #Agrego una propiedad para indicar que la ejecion de esta vista se realizo desde facturas.html
        context["t"] = "fc"
        #Valido que la accion que se esta tomando es la de editar un cliente
        if not pk:
            #En caso de que se este creando el cliente solo envio el formulario vacio
            form = ClienteForm()
        else:
            #Si se esta editando el cliente, traigo la data del cliente usando el parametro pk como filtro
            cliente = Cliente.objects.filter(id=pk).first()
            #Inicializo el formulario con la data del cliente 
            form = ClienteForm(instance=cliente)
            #Agrego la data del cliente a una propiedad del Json context
            context["obj"] = cliente
        #Agrego el formulario a una propiedad del Json context
        context["form"] = form
    else:
        #Almacenamiento de los datos que llegan del input id
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        celular = request.POST.get("celular")
        tipo = request.POST.get("tipo")
        usr = request.user

        #Valido si se esta creando un nuevo cliente o se esta editando
        if not pk:
            cliente = Cliente.objects.create(
                nombre = nombre,
                apellido = apellido,
                celular = celular,
                tipo = tipo,
                uc = usr
            )
        #Si se esta editando el registro de un cliente, se actualizara la data con la que llego en el request
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.celular = celular
            cliente.tipo = tipo
            cliente.um = usr.id
        
        #Forzo el guardado del cliente
        cliente.save()

        if not cliente:
            return HttpResponse("No se pudo Guardar/Crear Cliente")
        
        #Retorno el id del cliente al template
        id = cliente.id
        return HttpResponse(id)

    #Retorno el request y el objeto Json al template señalado
    return render(request, template_name, context)