import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt  # <-- Agrega esta línea

from .forms import *
from .models import Local, Foto, User

def register(request):
    # Registro básico con el User personalizado
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

   
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
            return HttpResponseRedirect(f'/insertar_foto/{local_id}')
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

def buscar(request):
    # Acepta ?q= o ?search=
    term = (request.GET.get('q') or request.GET.get('search') or '').strip()
    qs = Local.objects.all()

    if term:
        tokens = [t for t in term.split() if t]
        for t in tokens:
            qs = qs.filter(
                Q(direccion__icontains=t) |
                Q(provincia__icontains=t) |
                Q(municipio__icontains=t) |
                Q(sector__icontains=t) |
                Q(referencia__icontains=t) |
                Q(prop__icontains=t) |
                Q(user__username__icontains=t)
            )

    qs = qs.order_by('-id').distinct()
    total = qs.count()

    # Paginación
    p = Paginator(qs, 12)
    page = request.GET.get('page')
    locals_page = p.get_page(page)

    context = {
        "locals": locals_page,
        "buscar": term,
        "mensaje": f"Se encontraron {total} resultado(s) para '{term}'" if term else "Mostrando todas las propiedades",
        "count": total,
    }
    return render(request, "rentapp/buscar.html", context)

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

@login_required
def quien_es():
    pass

@login_required
def dashboard(request, id_user):
    locals = list(Local.objects.all().filter(user=id_user).order_by('-id')) 
    quien_es = User.objects.all().filter(id=id_user).values("phone", "id")[0]
    # local = Local.objects.all().filter(user=id_user).order_by('-id')
    
    p = Paginator(locals, 3)
    page = request.GET.get('page')
    local = p.get_page(page)

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

@login_required
def eliminar_foto(request, foto_id):
    """
    Elimina una foto por AJAX (POST). Verifica propiedad y borra el archivo físico.
    Respuestas:
      200: {"success": True}
      403: No autorizado
      405: Método no permitido
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    foto = get_object_or_404(Foto, id=foto_id)

    # Solo el dueño del local puede eliminar
    if foto.local.user != request.user:
        return JsonResponse({'success': False, 'message': 'No autorizado'}, status=403)

    # Borra archivo en disco si existe
    try:
        if foto.image_local and os.path.isfile(foto.image_local.path):
            os.remove(foto.image_local.path)
    except Exception:
        pass

    foto.delete()
    return JsonResponse({'success': True})

