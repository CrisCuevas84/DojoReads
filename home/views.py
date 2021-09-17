from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import Review, User, Libro, Autor


# Create your views here.
def home(request):
    reg_user = User.objects.get(id=request.session['user_id'])
    context = {
        "active_user": reg_user,
        'lista_libros': Libro.objects.all(),
    }
    return render(request, 'libros.html', context)


def agregar(request):
    context ={
        'autores': Autor.objects.all(),
    }
    return render(request, 'agregar.html', context)


def insertar(request):
    # Rescatando la info desde el Review
    # con variables errores, vamos a capturar errores
    errores = {}

    if int(request.POST['sautor']) == 0 and len(request.POST['autor']) == 0:
        errores['autor'] = "Debe seleccionar o crear un autor"  

    if len(request.POST['review']) == 0:
        errores['review'] = "Debe ingresar una reseña"

    if int(request.POST['rating']) == 0:
        errores['rating'] = "Debe seleccionar una calificación"

    if len(request.POST['titulo']) == 0:
        errores['titulo'] = "Debe ingresar un título"

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return render(request, 'agregar.html')
    else:
        if int(request.POST['sautor']) != 0:
        # Si es distinto de 0, viene el autor y tendremos que ir a buscarlo
            autor = Autor.objects.get(id=request.POST['sautor'])    
        elif len(request.POST['autor']) != 0:
            autor = Autor.objects.create(nombre=request.POST['autor'])
            book = Libro.objects.create(titulo = request.POST['titulo'], autor = autor, rating = request.POST['rating'])
            review = Review.objects.create(usuario = User.objects.get(id=request.session['user_id']), contenido = request.POST['review'], libro = book)
        return redirect('/libros/agregar')

    # Libro.objects.create(titulo = titulo, autor = autor, review = review, rating = rating)
    return render(request, 'agregar.html')


def recuperar(request):
    pass