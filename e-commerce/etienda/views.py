from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
from .forms import ProductoForm
import os
import logging
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import Http404



def consultaElectronica(request):
    resultados = consultaElectronicaEntre100y200()
    response = HttpResponse("<h1>Productos de Electrónica entre 100 y 200€:</h1>")

    for producto in resultados:
        response.write(f"<p>{producto['title']} - €{producto['price']}</p>")

    return response


def consultaDescripcion(request):
    resultados = consultaDescripcionPocket()
    response = HttpResponse(
        "<h1>Productos que contengan la palabra 'pocket' en la descripción:</h1>"
    )

    for producto in resultados:
        response.write(f"<p>{producto['title']} - {producto['description']}</p>")

    return response


def consultaPuntuacion(request):
    resultados = consultaPuntuacionMayorDe4()
    response = HttpResponse("<h1>Productos con puntuación mayor de 4:</h1>")

    for producto in resultados:
        response.write(f"<p>{producto['title']} - {producto['rating']['rate']}</p>")

    return response


def consultaHombrePuntuacion(request):
    resultados = consultaRopaHombrePorPuntuacion()
    response = HttpResponse("<h1>Ropa de hombre, ordenada por puntuación:</h1>")

    for producto in resultados:
        response.write(f"<p>{producto['title']} - {producto['rating']['rate']}</p>")

    return response


def consultaFacturacion(request):
    resultados = consultaFacturacionTotal()
    response = HttpResponse("<h1>Facturación total:</h1>")
    response.write(f"<p>La facturación total es: €{resultados}</p>")
    return response


def consultaFacturacionCategorias(request):
    resultados = consultaFacturacionPorCategoria()
    response = HttpResponse("<h1>Facturación por categoría de producto:</h1>")
    for categoria, facturacion in resultados.items():
        response.write(f"<p>{categoria}: €{facturacion}</p>")

    return response


def index(request):
    response = HttpResponse("<h1>Índice de Consultas:</h1>")
    response.write("<ul>")
    response.write(
        f"<li><a href='{reverse('cons-elec')}'>Consulta Electrónica entre 100 y 200€</a></li>"
    )
    response.write(
        f"<li><a href='{reverse('cons-desc')}'>Productos que contengan la palabra 'pocket' en la descripción</a></li>"
    )
    response.write(
        f"<li><a href='{reverse('cons-punt')}'>Productos con puntuación mayor de 4</a></li>"
    )
    response.write(
        f"<li><a href='{reverse('cons-homb-punt')}'>Ropa de hombre, ordenada por puntuación</a></li>"
    )
    response.write(
        f"<li><a href='{reverse('cons-fact-total')}'>Facturación total</a></li>"
    )
    response.write(
        f"<li><a href='{reverse('cons-fact-categoria')}'>Facturación por categoría de producto</a></li>"
    )
    response.write("</ul>")

    return response


def base(request):
    return render(request, "../templates/base.html")


def landingPage(request):

    return render(
        request,
        "../templates/landing.html"
    )


def categoriaProducto(request, cat_prod):
    if cat_prod == "mens-clothing":
        cat_prod = "men's clothing"
    elif cat_prod == "womens-clothing":
        cat_prod = "women's clothing"

    productos_categoria = productosCategoria(cat_prod)
    return render(
        request,
        "../templates/categoria.html",
        { "productos": productos_categoria},
    )


def busquedaPalabra(request):
    palabra = request.GET.get("palabra", "")
    resultados = []

    consulta = productos_collection.find(
        {
            "$or": [
                {"description": {"$regex": palabra, "$options": "i"}},
                {"title": {"$regex": palabra, "$options": "i"}},
                {"category": {"$regex": palabra, "$options": "i"}},
            ]
        }
    )
    
    for prod in consulta:
        producto = Producto(**prod)
        prod['id'] = str(prod['_id'])  # Accede directamente al _id de prod
        resultados.append(prod)

    if not resultados:
        messages.warning(request, "No se encontraron productos coincidentes.")
        return redirect('landingPage')

    return render(
        request, "busqueda.html", {"palabra": palabra, "resultados": resultados}
    )


def anadirProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = {
                'title': form.cleaned_data['title'],
                'price': form.cleaned_data['price'],
                'description': form.cleaned_data['description'],
                'category': form.cleaned_data['category'],
            }

            if not producto['title'][0].isupper():
                messages.error(request, 'El título debe comenzar con mayúscula.')
            else:
                # Guarda la imagen en la carpeta local "static/"
                imagen = form.cleaned_data['image']
                # Almacena la ruta relativa de la imagen en el campo 'image' del producto
                producto['image'] = imagen.name

                with open(os.path.join('static', imagen.name), 'wb') as destination:
                    for chunk in imagen.chunks():
                        destination.write(chunk)

                insertaProducto(producto)

                messages.success(request, 'Producto añadido correctamente')
                return redirect('landingPage')
        else:
            # En caso de que el formulario no sea válido
            messages.warning(request, 'Por favor, corrige los errores en el formulario.')

    else:
        form = ProductoForm()

    return render(request, 'anadir.html', {'form': form})

class Home(TemplateView):
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        return HttpResponseRedirect('/etienda/landing-page/')

def buscar_prod(id):
    producto = obtenerProducto(id)
    return producto