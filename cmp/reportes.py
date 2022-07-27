import os
from urllib import response
from urllib.parse import urljoin
from django.conf import settings
from django.http import HttpResponse
from django.template import context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone

#Importacion de los modelos ComprasEnc y ComprasDec del archivo models.py
from .models import ComprasEnc, ComprasDet

def link_callback(url, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resource
    """

    # use short variable names
    sUrl = settings.STATIC_URL      #typically /static/
    sRoot = settings.STATIC_ROOT    #typically /home/suerX/project_static/
    mUrl = settings.MEDIA_URL       #typically /static/media/
    mRoot = settings.MEDIA_ROOT     #typically /home/userX/project_static/media/

    #convert URIs to absolute system paths
    if uri.startswitch(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswitch(sUrl):
        path = os.path.join(sRoot, uri.replace(Surl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    
    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start width %s or %s' % (sUrl, mUrl)
            )
    return path

#funcion que imprimira todas las compras
def reporte_compras(request):
    #ruta del template
    template_path = 'cmp/compras_print_all.html'
    #Fecha de creacion
    today = timezone.now()

    #Filtrado de las compras
    compras = ComprasEnc.objects.all()
    #Creacion del Json contexto que se enviara al template
    contexto = {
        'obj': compras,
        'today': today,
        'request': request
    }

    #Objeto respuesta de tipo pdf
    response = HttpResponse(content_type = 'application/pdf')
    #Asignacion de la forma en que se mostrara, Se Configurar para que se muetre en pantalla y no directamente en descarga
    response['Content-Disposition'] = 'inline; filename = "todas_compras.pdf"'

    #Renderizacion de la plantilla
    template = get_template(template_path)
    #Renderizacion del contexto a la plantilla renderizada
    html = template.render(contexto)

    #Creacion del pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    #Si hay un error se mostrara un mensaje en pantalla
    if pisaStatus.err:
        return HttpResponse('A ocurrido un error <pre>' + html + '</pre>')

    return response

#Funcion que imprimira una sola compra en un archivo pdf
def imprimir_compra(request, compra_id):
    #Variable con la ruta template
    template_path = 'cmp/compra_print_one.html'
    #Fecha en la que se creara el pdf
    today = timezone.now()

    #Captura del registro en la tabla CompraEnc usando el parametro compra_id como filtro
    enc = ComprasEnc.objects.filter(id = compra_id).first()

    #Evaluo si el objeto enc no es nulo
    if enc:
        #Busco el registro dentro de la tabla CopmprasDet donde el valor de compra_id coincida con la propiedad id de compra
        detalle = ComprasDet.objects.filter(compra__id = compra_id)
    else:
        detalle = {}

    #Objeto que se enviara al template
    contexto = {
        'detalle': detalle,
        'encabezado': enc,
        'today': today,
        'request': request
    }

    #Objeto respuesta de tipo pdf
    response = HttpResponse(content_type = 'application/pdf')
    #Asignacion de la forma en que se mostrara, Se Configurar para que se muetre en pantalla y no directamente en descarga
    response['Content-Disposition'] = 'inline; filename = "todas_compras.pdf"'

    #Renderizacion de la plantilla
    template = get_template(template_path)
    #Renderizacion del contexto a la plantilla renderizada
    html = template.render(contexto)

    #Creacion del pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    #Si hay un error se mostrara un mensaje en pantalla
    if pisaStatus.err:
        return HttpResponse('A ocurrido un error <pre>' + html + '</pre>')

    return response