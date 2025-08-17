import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Header
from fastapi.params import Depends
import psycopg2
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop_schema import LaptopBase
from api.db.models.laptop_model import Laptop
from api.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/laptops")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[LaptopBase])
def list_laptops(limit: int = 20, db: Session = Depends(get_db)):
    laptops = db.query(Laptop).limit(limit).all()
    if not laptops:
        raise HTTPException(status_code=404, detail="No laptops found")
    return laptops

@router.get("/{id}", response_model=LaptopBase)
def get_laptop_detail(id: str, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop

@router.get("/recommendations/hybrid")
def get_hybrid_recommendations(
    user_id: Optional[str] = Query(None),
    fingerprint: str = Query(..., description="User fingerprint from tracking"),
    limit: int = Query(10, ge=1, le=50),
    collaborative_weight: float = Query(0.6, ge=0.0, le=1.0),
    content_weight: float = Query(0.4, ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """
    Get hybrid recommendations combining collaborative and content-based filtering
    """
    # Validate weights sum to 1
    if abs(collaborative_weight + content_weight - 1.0) > 0.01:
        raise HTTPException(
            status_code=400, 
            detail="Collaborative and content weights must sum to 1.0"
        )
    
    # Use user_id if available, otherwise use fingerprint
    user_identifier = user_id if user_id else fingerprint
    
    recommendation_service = RecommendationService(db)
    recommendations = recommendation_service.get_hybrid_recommendations(
        user_identifier=user_identifier,
        limit=limit,
        collaborative_weight=collaborative_weight,
        content_weight=content_weight
    )
    
    if not recommendations:
        # Fallback to popular laptops if no recommendations
        popular_laptops = db.query(Laptop).limit(limit).all()
        recommendations = [
            {
                "laptop": laptop,
                "recommendation_score": 0.5,
                "reason": "Popular choice"
            }
            for laptop in popular_laptops
        ]
    
    return {
        "recommendations": recommendations,
        "algorithm": "hybrid",
        "weights": {
            "collaborative": collaborative_weight,
            "content": content_weight
        }
    }

@router.post("/track-interaction")
def track_interaction(
    laptop_id: str,
    interaction_type: str,
    user_id: Optional[str] = None,
    fingerprint: str = Query(...),
    session_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Track user interaction for recommendation system
    """
    recommendation_service = RecommendationService(db)
    recommendation_service.record_interaction(
        user_id=user_id,
        fingerprint=fingerprint,
        session_id=session_id,
        laptop_id=laptop_id,
        interaction_type=interaction_type
    )
    
    return {"status": "interaction recorded"}