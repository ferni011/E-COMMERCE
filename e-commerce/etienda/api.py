# tienda/api.py
from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema,Form,Body
from ninja.security import HttpBearer
import logging
from bson.objectid import ObjectId
from .views import *
from django.shortcuts import get_object_or_404
from .models import Producto
from bson.errors import InvalidId
from pymongo import ReturnDocument
from typing import List


logger = logging.getLogger(__name__)

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "root":
            return token

api = NinjaExtraAPI(auth=GlobalAuth())
	
# auth=GlobalAuth()

class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Rate] = None
	
	
class ErrorSchema(Schema):
	message: str

class MensajeSchema(Schema):
    message: str

class RatingUpdateSchema(Schema):
    new_rating: float

class RatingResponseSchema(Schema):
    rate: float
    count: int


	
# GET DETALLE DE UN PRODUCTO
@api.get("/productos/{id}", tags=['TIENDA DAI'], response={200: ProductSchema, 404: ErrorSchema})
def obtener_producto(request, id: str):
    try:
        producto = buscar_prod(ObjectId(id))
        if producto is None:
            return 404, {'message': 'no encontrado'}
        else:
            producto["id"] = str(producto.get('_id'))
            del producto["_id"]
            return 200, producto
    except InvalidId:
        return 404, {'message': 'no encontrado'}
    


# AÑADIR UN PRODUCTO
@api.post("/productos", tags=['TIENDA DAI'], response={200: ProductSchema, 400: ErrorSchema})
def añadir_producto(request, item: ProductSchemaIn = Form(...)):
    try:
        producto_id = productos_collection.insert_one(item.dict()).inserted_id
        producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
        producto["id"] = str(producto.get('_id'))
        del producto["_id"]
        return 200, producto
    except Exception as e:
        return 400, {'message': str(e)}
    
# BORRAR UN PRODUCTO
@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={200: MensajeSchema, 404: ErrorSchema})
def borrar_producto(request, id:str):
    try:
        producto = buscar_prod(ObjectId(id))
        if producto is None:
            return 404, {'message': 'no encontrado'}
        else:
            productos_collection.delete_one({"_id": ObjectId(id)})
            return 200, {'message': 'borrado'}
    except InvalidId:
        return 404, {'message': 'no encontrado'}
    


# GET lista productos con paginador
@api.get("/productos", tags=['TIENDA DAI'], response={200: List[ProductSchema], 404: ErrorSchema})
def obtener_productos_paginador(request, desde: int = 0, hasta: int = 4):
    try:
        productos = productos_collection.find().skip(desde).limit(hasta)
        lista_productos = []
        for producto in productos:
            producto["id"] = str(producto.get('_id'))
            del producto["_id"]
            lista_productos.append(producto)
        return 200, lista_productos
    except Exception as e:
        return 400, {'message': str(e)}
    

# MODIFICAR PRODUCTO
@api.put("/productos/{id}", tags=['TIENDA DAI'], response={200: ProductSchema, 400: ErrorSchema, 404: ErrorSchema})
def modificar_producto(request, id: str, item: ProductSchemaIn = Body(...)):
    try:
        producto = productos_collection.find_one({"_id": ObjectId(id)})
        if producto is None:
            return 404, {'message': 'no encontrado'}
        else:
            # Actualiza sólo los campos proporcionados en item
            campos_a_actualizar = {k: v for k, v in item.dict().items() if v is not None}
            producto_actualizado = productos_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": campos_a_actualizar}, return_document=ReturnDocument.AFTER)
            producto_actualizado["id"] = str(producto_actualizado.get('_id'))
            del producto_actualizado["_id"]
            return 200, producto_actualizado
    except InvalidId:
        return 404, {'message': 'no encontrado'}
    except Exception as e:
        return 400, {'message': str(e)}
    

# Actualizar calificación producto
@api.post("/productos/{id}/rating", tags=['TIENDA DAI'], response={200: MensajeSchema, 400: ErrorSchema, 404: ErrorSchema})
def actualizar_calificacion(request, id: str, rating_update: RatingUpdateSchema):
    try:
        producto = productos_collection.find_one({"_id": ObjectId(id)})
        if producto is None:
            return 404, {'message': 'Producto no encontrado'}

        # Calcula la nueva calificación
        total_rating = producto["rating"]["rate"] * producto["rating"]["count"]
        total_rating += rating_update.new_rating
        producto["rating"]["count"] += 1
        producto["rating"]["rate"] = total_rating / producto["rating"]["count"]

        # Actualiza el producto en la base de datos
        productos_collection.update_one({"_id": ObjectId(id)}, {"$set": producto})

        return 200, {"message": "Calificación actualizada correctamente"}
    except Exception as e:
        return 400, {'message': str(e)}
    

# Devolver calificación media y numero de votos
@api.get("/productos/{id}/rating", tags=['TIENDA DAI'], response={200: RatingResponseSchema, 404: ErrorSchema})
def get_calificacion_votos(request, id: str):
    try:
        producto = productos_collection.find_one({"_id": ObjectId(id)})
        if producto is None:
            return 404, {'message': 'Producto no encontrado'}
        
        return 200, {"rate": producto['rating']['rate'], "count": producto['rating']['count']}
    except Exception as e:
        return 400, {'message': str(e)}