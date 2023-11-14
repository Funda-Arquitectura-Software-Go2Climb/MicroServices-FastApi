from fastapi import APIRouter, HTTPException
from config.db import conn
from bson import ObjectId
from httpx import AsyncClient
from schemas.agencyReview_schema import agencyReviewEntity, Entity

from models.agencyReview_model import AgencyReview_model

agency_review = APIRouter()

@agency_review.get('/agency_reviews')
async def find_all_reviews():
    reviews = Entity(conn.mydatabase.agency_reviews.find())

    async with AsyncClient() as client:
        for review in reviews:
            # Obtiene el ID del turista de la revisión
            tourist_id = review.get('tourist')

            if tourist_id:
                # Realiza una solicitud GET al endpoint de Express para obtener el turista
                express_url = f'http://localhost:3000/tourists/{tourist_id}'
                response = await client.get(express_url)
                tourist_data = response.json() if response.status_code == 200 else None
                review['tourist'] = tourist_data

    return reviews



@agency_review.post('/agency_reviews')
def create_review(review: AgencyReview_model):
    new_review = review.dict()
    del new_review["id"]  # El ID será generado por MongoDB
    inserted_id = conn.mydatabase.agency_reviews.insert_one(new_review).inserted_id
    return {"id": str(inserted_id)}


@agency_review.get('/agency_reviews/{id}')
async def find_review(id: str):
    review = conn.mydatabase.agency_reviews.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Obtiene el ID del turista de la revisión
    tourist_id = review.get('tourist')

    if tourist_id:
        # Define la URL del endpoint de Express para obtener el turista
        express_url = f'http://localhost:3000/tourists/{tourist_id}'

        async with AsyncClient() as client:
            # Realiza una solicitud GET al endpoint de Express
            response = await client.get(express_url)
            tourist_data = response.json() if response.status_code == 200 else None
            review['tourist'] = tourist_data

    return agencyReviewEntity(review)


@agency_review.put('/agency_reviews/{id}')
def update_review(id: str, review_data: AgencyReview_model):
    review = conn.mydatabase.agency_reviews.find_one({"_id": ObjectId(id)})
    if review:
        update_data = review_data.dict(exclude_unset=True) # Convertir el modelo a diccionario y excluir campos no establecidos
        if "id" in update_data:  # No queremos actualizar el id
            del update_data["id"]
        conn.mydatabase.agency_reviews.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return {"status": "Review updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@agency_review.delete('/agency_reviews/{id}')
def delete_review(id: str):
    review = conn.mydatabase.agency_reviews.find_one({"_id": ObjectId(id)})
    if review:
        conn.mydatabase.agency_reviews.delete_one({"_id": ObjectId(id)})
        return {"status": "Review deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@agency_review.get('/tourists/{id}')
async def get_tourist_by_id(id: str):
    # Define la URL del endpoint de Express http://localhost:3000/tourists/1
    express_url = f'http://localhost:3000/tourists/{id}'

    async with AsyncClient() as client:
        # Realiza una solicitud GET al endpoint de Express
        response = await client.get(express_url)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Devuelve la respuesta de Express
        return response.json()
    elif response.status_code == 404:
        # Si el recurso no se encuentra en Express, devuelve un error 404 en FastAPI
        raise HTTPException(status_code=404, detail="Tourist not found")
    else:
        # Maneja otros códigos de estado de error según sea necesario
        raise HTTPException(status_code=500, detail="An error occurred in the external service")