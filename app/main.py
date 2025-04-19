from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, database
from .recommender import ContentRecommender
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Netflix-like Recommendation System")

# Initialize recommender
recommender = ContentRecommender()

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: str
    #password: str

class ContentCreate(BaseModel):
    title: str
    description: str
    content_type: str
    genre: str
    release_year: int
    rating: float

class ContentResponse(BaseModel):
    id: int
    title: str
    description: str
    content_type: str
    genre: str
    release_year: int
    rating: float

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email
       #hashed_password=user.password  # In production, hash the password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/content/", response_model=ContentResponse)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    db_content = models.Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@app.post("/users/{user_id}/watch/{content_id}")
def mark_content_watched(user_id: int, content_id: int, rating: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    content = db.query(models.Content).filter(models.Content.id == content_id).first()
    
    if not user or not content:
        raise HTTPException(status_code=404, detail="User or content not found")
    
    # Add to watch history
    user.watched_content.append(content)
    db.commit()
    return {"message": "Content marked as watched"}

@app.get("/users/{user_id}/recommendations", response_model=List[ContentResponse])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommended_content = recommender.recommend_content(db, user_id)
    return recommended_content

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 