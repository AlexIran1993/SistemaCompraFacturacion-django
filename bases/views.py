from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from .models import Idioma, Frase

# Create your views here.
#Mixin que validara los formularios 
class MixinFormInvalid:
    #Sobrescritura de form_invalid
    def form_invalid(self, form):
        #Instancia del formulario invalio que proviene de cleaned
        response = super().form_invalid(form)

        #Se valida que el formulario provenga por parte de ajax
        if self.request.is_ajax():
            #Si se cumple la validacion, se envia un response con el error y el status en 400
            return JsonResponse(form.erros, status=400)
        else:
            response

#Clase que controlara a los usuario con privilegios limitados
class SinPrivilegios(LoginRequiredMixin ,PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    #Evito que se levante el error 404 forbiden
    raise_execpction = False
    redirect_file_name = "redirect to"

    #Modifico el metodo que redirecciona a los usuaris
    def handle_no_permission(self):
        #Valido que el usuaro no sea anonimo:
        if not self.request.user == AnonymousUser():
            #Especifico el path de la aplicacin bases.
            self.login_url = 'bases:sin_privilegios'
            
        #Retorno al template sin_privilegios
        return HttpResponseRedirect(reverse_lazy(self.login_url))


#Vista generica
class Home(LoginRequiredMixin, generic.TemplateView):
    #Directorio de l plantilla
    template_name = 'bases/home.html'
    #Variable que valida la authenticacion del usuario, en caso de que no este validado lo redireccionara
    #al url señalado en la variable login_url.
    login_url = 'bases:login'

#Vista que mostrar la plantilla en caso de que el usuario intente ingresar a una seccion sin privilegios
class HomeSinPrivilegios(LoginRequiredMixin ,generic.TemplateView):
    login_url = "bases:login"
    template_name = "base/sin_privilegios.html"


class IdiomaList(generic.ListView):
    template_name = "bases/idiomas_list.html"
    model = Idioma
    context_object_name = "obj"

class FraseList(generic.ListView):
    template_name = "bases/frase_list.html"
    model = Frase
    context_object_name = "obj"

    #Sobre escritura de la lista con los registros de Frase
    def get_queryset(self):
        #Traigo todos los registros de Frase
        qs = Frase.objects.all()
        #Extraigo el parametro que se envio desde idioma_list.html
        idioma_id = self.request.GET.get("lang")
        #Valido que el parametro sea true
        if idioma_id:
            #Aplico un filtro a la lista qs comparando la propiedad id del foreingkey idioma
            qs = qs.filter(idioma__id = idioma_id)
        #Retorno la lista de frases a el template.
        return qs