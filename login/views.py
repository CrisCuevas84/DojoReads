from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

from .models import * # vamos a trabajar también con clase Poke

# Create your views here.
def login(request):
    # Preguntar si hay un usuario en session
    if 'user_id' in request.session:
        return redirect('libros/')

    # return render(request, 'regpoke2.html')
    return render(request, 'registro.html')

def registrar(request):
    return render(request, 'registro.html')


def inicio(request):
    usuario = User.objects.filter(email=request.POST['email'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('libros/')

def registro(request): # para caprturar vairable request se hace request.post['nombrevariable']
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password']) # Este post trae todo
        decode_hash_pw = password.decode('utf-8')
        #crear usuario

        rol = 2
        if User.objects.all().count() == 0:
            rol = 1
        user = User.objects.create(
            nombre=request.POST['nombre'], # Este Post trae algo en especifico
            alias=request.POST['alias'],
            email=request.POST['email'],
            password=decode_hash_pw,
            rol=rol,
        )
        # request.session['user_id'] = user.id
        # retornar mensaje de creación correcta
        msg="Usuario creado exitosamente!"
        messages.success(request, msg)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')