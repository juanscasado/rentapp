import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.core.paginator import Paginator
from django.shortcuts import  render
# from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import  HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout

# filepath: /c:/Users/WinFree/Desktop/repo/rentapp/rentapp/views.py
from django.shortcuts import render, redirect
from .forms import LocalForm

from django.contrib.auth import login, authenticate

from .forms import UserForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Authenticate and login the user
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, new_user)
            return redirect(f'/dashboard/{user.id}')  # Redirect to a success page.
    else:
        form = UserForm()
    return render(request, 'registration/registration_form.html', {'form': form})
# def editar_renta(request, renta_id):
#     renta = get_object_or_404(Renta, id=renta_id)
#     if request.method == 'POST':
#         form = RentaForm(request.POST, instance=renta)
#         if form.is_valid():
#             form.save()
#             return redirect('rentapp:detail', renta_id=renta.id)
#     else:
#         form = RentaForm(instance=renta)
#     return render(request, 'rentapp/editar_renta.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

# def insertar_mensaje(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = MensajeForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             new_mensaje = Mensaje(
#                 amistad = form.cleaned_data['amistad'],
#                 texto = form.cleaned_data['texto'],
#                 tipo = 'rendador',
#                 pub_date = time.strftime('%Y-%m-%d %I:%M')
#                  )
#             new_mensaje.save()
#             # redirect to a new URL:
#             return HttpResponseRedirect('/rentapp/insertar_mensaje/')
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         # print (datos)
#         form = MensajeForm()
#     return render(request, 'rentapp/insertar_mensaje.html', {'form': form, })

# def insertar_mensaje_rendatario(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = MensajeForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             new_mensaje = Mensaje(
#                 amistad = form.cleaned_data['amistad'],
#                 texto = form.cleaned_data['texto'],
#                 tipo = 'rendatario',
#                 pub_date = time.strftime('%Y-%m-%d %I:%M')
#                  )
#             new_mensaje.save()
#             # redirect to a new URL:
#             return HttpResponseRedirect('/rentapp/insertar_mensaje_rendatario/')
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         datos_amistad = list(Amistad.objects.values().order_by("-id"))
#         datos = list(Mensaje.objects.values().order_by("-id"))
#         # print (datos)
#         form = MensajeForm()
#     return render(request, 'rentapp/insertar_mensaje_rendatario.html', {'form': form, 'datos': datos, 'datos_amistad': datos_amistad })

# def insertar_amistad(request, usertario_id, userdador_id, renta_id):
#     existe_amistad = Amistad.objects.filter(usertario=usertario_id,userdador=userdador_id, renta=renta_id).values_list()
#     # if(existe_amistad):
#     #     return HttpResponse("Si existe")
#     # else:
#     #     return HttpResponse("No existe")
#     # return HttpResponse(existe_amistad[0][0])
#     if existe_amistad:
#           return HttpResponseRedirect(f"/chat/{existe_amistad[0][0]}")
#     else:
#           renta = Renta.objects.get(id=renta_id)
#           usertario = Usertario.objects.get(id=usertario_id)
#           userdador = Userdador.objects.get(id=userdador_id)

#           f = AmistadForm()
#           new_amistad = f.save(commit=False)
#           new_amistad.renta = renta
#           new_amistad.usertario = usertario #12
#           new_amistad.userdador = userdador #12,
#           new_amistad.relacion = f'{usertario}:{ renta}'
#           new_amistad.pub_date = time.strftime('%Y-%m-%d %I:%M')
#           new_amistad.save()
#           # get the last 'id'
#           obj = Amistad.objects.latest('id')
#           # redirect to a new URL:
#           return HttpResponseRedirect(f"/chat/{obj}")
   
def insertar_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = User(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'],
                tipo = form.cleaned_data['phone_number'], )
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponseRedirect(f'/dashboard/{user.id}')
    # if a GET (or any other method) we'll create a blank form
    else:

        #datos = list(Usertario.objects.values().order_by("-id"))
        form = UserForm()
    mensajes = messages.success(request, "Por favor inicie session o cuenta nueva")

    return render(request, 'rentapp/insertar_user.html', {'mensajes':mensajes,'form': form})

@login_required
@csrf_exempt
def insertar_foto(request, local_id):
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_foto = form.save(commit=False)
            new_foto.local_id = local_id
            new_foto.save()
            return JsonResponse({'id': new_foto.id, 'image_local': new_foto.image_local.url})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        datos_fotos = list(Foto.objects.filter(local=local_id).order_by("-id"))
        local_title = list(Local.objects.filter(id=local_id))
        form = FotoForm()
        return render(request, 'rentapp/insertar_foto.html', {'renta_title': local_title, 'local_id': local_id, 'datos_fotos': datos_fotos, 'form': form})
    

@login_required
def obtener_fotos(request, local_id):
    datos_fotos = list(Foto.objects.filter(local=local_id).order_by("-id"))
    fotos = [{'id': foto.id, 'image_local': foto.image_local.url} for foto in datos_fotos]
    return JsonResponse({'fotos': fotos})
# @login_required
# def insertar_foto(request, local_id):
#     datos_fotos = list(Foto.objects.filter(local=local_id).order_by("-id"))
#     local_title = list(Local.objects.filter(id=local_id))
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = FotoForm(request.POST, request.FILES)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             new_foto = Foto(
#                 local = form.cleaned_data['local'],
#                 image_local = form.cleaned_data['image_local'],
#                 name_foto_local = form.cleaned_data['name_foto_local'])
#             new_foto.save()
#             # obj = Foto.objects.latest('renta')
#             # renta_id = obj
#             # redirect to a new URL:
#             return HttpResponseRedirect(f'/insertar_foto/{local_id}')
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         # obj = Foto.objects.latest('renta')
#         form = FotoForm()
#         # datos_fotos = list(Foto.objects.all().order_by("-id"))
#     return render(request, 'rentapp/insertar_foto.html', {'renta_title':local_title,'local_id':local_id,'datos_fotos': datos_fotos, 'form': form})

@login_required
def insertar_local(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            provincia_nombre = form.cleaned_data['provincia'].split('.')
            municipio_nombre =  form.cleaned_data['municipio'].split('.')
            #num_calle = form.cleaned_data['direccion']
            #direccion_full = f"{form.cleaned_data['direccion']}, {form.cleaned_data['sector']}, DO."
            direccion_full = f"{form.cleaned_data['direccion']}, {form.cleaned_data['sector']}, {municipio_nombre[1]}, {provincia_nombre[1]}, República Dominicana"
            # geolocator = Nominatim(user_agent="rentapp", timeout=10)
            # location = geolocator.geocode(direccion_full)
            # location = ""

            # process the data in form.cleaned_data as required
            # ...
            new_local = Local(
                user = form.cleaned_data['user'],
                direccion = direccion_full,
                sector = form.cleaned_data['sector'],
                municipio = municipio_nombre[1],
                provincia = provincia_nombre[1],
                referencia = form.cleaned_data['referencia'],
                prop = form.cleaned_data['prop'],

                # pub_date = time.strftime('%Y-%m-%d %I:%M'),
                )
            new_local.save()
            obj = Local.objects.latest('id')
            renta_id = obj

            # renta_direccion = obj.direccion
            # obj = Amistad.objects.latest('id')

            # redirect to a new URL:
            return HttpResponseRedirect(f'/insertar_foto/{renta_id.id}')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocalForm()
    return render(request, 'rentapp/insertar_local.html', {'form': form})

def index(request):
    locals = list(Local.objects.all().order_by('-id'))
    fotos_local = list(Foto.objects.all().values().order_by('-id'))
    # fotos_rentas = list(Foto.objects.all().select_related('renta').values(
    #     'renta__usertario', 'renta__id', 'renta__direccion',
    #     'id', 'image_renta', 'name_foto_renta').order_by('-id'))
    p = Paginator(locals, 6)
    page = request.GET.get('page')
    local = p.get_page(page)

    context = {
        "fotos_local":fotos_local,
        "local": local,
    }
    return render(request, "rentapp/index.html", context)

@login_required
def detail(request, local_id):

    try:
        fotos = Foto.objects.filter(local=local_id)
        local_location = Local.objects.get(pk=local_id)
        # geolocator = Nominatim(user_agent="rentapp", timeout=10)
        # location = geolocator.geocode(renta_location.direccion)
        location = ""

    except Exception as e:
       return HttpResponse(f'ahora si :{e}' )
    context = {
            "fotos" : fotos,
            "location" : location,
            "local_location" : local_location,
        }
    return render(request, "rentapp/detail.html", context)

# Reparar
def buscar(request):
    # br = Renta.objects.all()
    if 'buscar' in request.method:
        b = request.post(request, "buscar")
        q_local = Local.objects.filter(direccion__search = b)
    else:
        q_local = Local.objects.all().order_by('-id')
        p = Paginator(q_local, 5)
        page = request.GET.get("page")
        local = p.get_page(page)
        context = {
        "local" : local,
        "fotos" : list(Foto.objects.values()),
        }
        response = render(request, "rentapp/buscar.html", context )
        return response

@login_required
def quien_es():
    pass

@login_required
def dashboard(request, id_user):
    quien_es = User.objects.all().filter(id=id_user).values("phone", "id")[0]
    # tener todas las rentas del usuario
    local = Local.objects.all().filter(user=id_user).order_by('-id')
    # user_app = User.objects.all().filter(usertario=id_rendatario).order_by('-id')
    print(quien_es)
    print(local)
    context = {
        "quien_es": quien_es,
        "local": local,
    }
    return render(request, "rentapp/dashboard.html", context)

@login_required
def delete_local(request, id_local, user):
    # Obtener todas las fotos asociadas al local
    fotos = Foto.objects.filter(local=id_local)
    
    # Eliminar los archivos de las fotos del sistema de archivos
    for foto in fotos:
        if foto.image_local:
            image_path = os.path.join(settings.MEDIA_ROOT, str(foto.image_local))
            if os.path.exists(image_path):
                os.remove(image_path)
    
    # Eliminar las fotos de la base de datos
    fotos.delete()
    
    # Eliminar el local
    local = Local.objects.filter(id=id_local)
    local.delete()
    
    return HttpResponseRedirect(f"../dashboard/{user}")

def prueba(request):

    # amistad_userdador = Amistad.objects.filter(userdador = userdador_id).select_related('renta','usertario','userdador').values(
    #     'renta', 'userdador', 'usertario').order_by('-id')    # id, mensaje, pub_date, relacion, userdador, userdador_id, usertario, usertario_id
    # # amistad = Amistad.objects.filter(userdador=userdador_id).values("id", 'pub_date', 'relacion', 'userdador', 'usertario',)
    local = list(Local.objects.all().values())
    fotos_local = list(Foto.objects.all().values())

    return  HttpResponse(f"local: {local}----Fotos:{fotos_local}" )

