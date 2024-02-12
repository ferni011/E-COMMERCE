from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError, validator
import pathlib
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any, Optional
import requests
from django.utils.text import slugify
import os
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.models import model_to_dict
from decimal import Decimal
from bson.objectid import ObjectId




# https://requests.readthedocs.io/en/latest/
def getProductos(api):
    response = requests.get(api)
    return response.json()


# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/


# Adaptamos la clase Nota para los de la fake API
class Nota(BaseModel):
    rate: float = Field(ge=0.0, lt=5.0)
    count: int = Field(ge=1)


# Adaptamos la clase Producto para los de la fake API
class Producto(BaseModel):
    #_id: Any
    title: str
    price: float
    description: str
    category: str
    image : str | None
    rating: Nota = None


    # Añadir una validación adiccional para asegurarse que el contenido en el campo 'nombre' empieza por mayúscula
    @validator('title')
    def validate_title(cls, value):
        if not value[0].isupper():
            raise ValueError("La primera letra del título debe ser mayúscula")
        return value

#Clase compra
class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list
        


# Conexión con la BD
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient("mongo", 27017)

tienda_db = client.tienda  # Base de Datos
productos_collection = tienda_db.productos  # Colección
compras_collection = tienda_db.compras  # Colección

def insertaProducto(producto):
    prod = Producto(**producto)
    # Inserta la ruta de la imagen en el campo 'image' del producto
    prod.image = producto['image']
    productos_collection.insert_one(prod.dict())



def insertaCompra(compra):
    comp = Compra(**compra)
    compras_collection.insert_one(comp.dict())


# Insertar productos
# productos = getProductos('https://fakestoreapi.com/products')
# for p in productos:
#     producto = Producto(**p)
#     productos_collection.insert_one(producto.model_dump())


# Electrónica entre 100 y 200€, ordenados por precio


def consultaElectronicaEntre100y200():
    productos = []
    consulta = productos_collection.find(
        {"$and": [{"price": {"$gt": 100, "$lt": 200}}, {"category": "electronics"}]}
    ).sort("price")

    for prod in consulta:
        productos.append(prod)

    return productos


# Productos que contengan la palabra 'pocket' en la descripción
def consultaDescripcionPocket():
    productos = []
    for prod in productos_collection.find(
        {"description": {"$regex": "pocket", "$options": "i"}}
    ):
        productos.append(prod)  # Agrega cada producto a la lista de resultados
    return productos  # Devuelve la lista de productos


# Productos con puntuación mayor de 4


def consultaPuntuacionMayorDe4():
    productos = []
    for prod in productos_collection.find({"rating.rate": {"$gt": 4}}):
        productos.append(prod)

    return productos


# Ropa de hombre, ordenada por puntuación


def consultaRopaHombrePorPuntuacion():
    productos = []
    consulta = productos_collection.find({"category": "men's clothing"}).sort(
        "rating.rate"
    )

    for prod in consulta:
        productos.append(prod)

    return productos


# Facturación total


def consultaFacturacionTotal():
    facturacion_total = 0.0
    for compra in compras_collection.find({}):
        for prod in compra["productos"]:
            prodenc = productos_collection.find_one({"_id": prod})
            if prodenc is not None:
                facturacion_individual = prodenc["price"]
                facturacion_total += facturacion_individual

    return facturacion_total


# Facturación por categoría de producto


def consultaFacturacionPorCategoria():
    facturacion_categorias = {}

    for compra in compras_collection.find({}):
        for prod in compra["productos"]:
            prodenc = productos_collection.find_one({"_id": prod})
            if prodenc is not None:
                if prodenc["category"] in facturacion_categorias:
                    facturacion_categorias[prodenc["category"]] += prodenc["price"]
                else:
                    facturacion_categorias[prodenc["category"]] = prodenc["price"]

    return facturacion_categorias


# Categorias distintas


def obtenerCategorias():
    categorias_distintas = productos_collection.distinct("category")
    return categorias_distintas


# Para tener un slug válido para las urls
def obtenerCategoriasSinEspacios():
    categorias = obtenerCategorias()
    categorias_sin_espacios = []

    for categoria in categorias:
        categoria_formateada = slugify(categoria)
        categorias_sin_espacios.append(categoria_formateada)

    return categorias_sin_espacios


# Obtener productos de cada categoría


def productosCategoria(categoria):
    productos = []
    consulta = productos_collection.find({"category": categoria})
    for prod in consulta:
        producto = Producto(**prod)
        prod['id'] = str(prod['_id'])  # Accede directamente al _id de prod
        productos.append(prod)

    return productos


# Obtener producto por ID

def obtenerProducto(id):
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    return producto