from fastapi import FastAPI
from routes.agencyReview_routes import agency_review
app = FastAPI()

app.include_router(agency_review)