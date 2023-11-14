def agencyReviewEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "date": item["date"],
        "comment": item["comment"],
        "professionalism_score": item["professionalism_score"],
        "security_score": item["security_score"],
        "quality_score": item["quality_score"],
        "cost_score": item["cost_score"],
        "customers_id": item["customers_id"],
        "tourist": item["tourist"]
    }

    
def Entity(entity) -> list:
    return [agencyReviewEntity(item) for item in entity]