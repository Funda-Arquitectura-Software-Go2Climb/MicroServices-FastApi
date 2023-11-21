from fastapi import APIRouter, HTTPException
from config.db import conn
from bson import ObjectId
from httpx import AsyncClient
from schemas.agencyReview_schema import agencyReviewEntity, Entity
from models.agencyReview_model import AgencyReview_model

agency_review = APIRouter()

async def fetch_agency_data(agency_id: str):
    express_url = f'https://agencymicro.azurewebsites.net/api/v1/agencies/{agency_id}'
    async with AsyncClient() as client:
        try:
            response = await client.get(express_url)
            if response.status_code == 200:
                agency_data = response.json()
                agency_data.pop('services', None)
                return agency_data
        except Exception as e:
            print(f"Error fetching agency data: {e}")
        return agency_id

async def fetch_tourist_data(tourist_id: str):
    express_url = f'https://touristrepo.onrender.com/tourists/{tourist_id}'
    async with AsyncClient() as client:
        try:
            response = await client.get(express_url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching tourist data: {e}")
        return tourist_id

@agency_review.get('/agency_reviews')
async def find_all_reviews():
    reviews = Entity(conn.mydatabase.agency_reviews.find())
    for review in reviews:
        if 'agency' in review and review['agency']:
            review['agency'] = await fetch_agency_data(review['agency'])
        if 'tourist' in review and review['tourist']:
            review['tourist'] = await fetch_tourist_data(review['tourist'])
    return reviews

@agency_review.get('/agency_reviews/{id}')
async def find_review(id: str):
    review = conn.mydatabase.agency_reviews.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if 'agency' in review and review['agency']:
        review['agency'] = await fetch_agency_data(review['agency'])
    if 'tourist' in review and review['tourist']:
        review['tourist'] = await fetch_tourist_data(review['tourist'])
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
    
@agency_review.post('/agency_reviews')
def create_review(review: AgencyReview_model):
    new_review = review.dict()
    del new_review["id"]  # El ID será generado por MongoDB
    inserted_id = conn.mydatabase.agency_reviews.insert_one(new_review).inserted_id
    return {"id": str(inserted_id)}

