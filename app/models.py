from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# User-Content many-to-many relationship table
user_content_association = Table(
    'user_content_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('content_id', Integer, ForeignKey('content.id')),
    Column('rating', Float),
    Column('watched_at', DateTime, default=datetime.utcnow)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with content through watch history
    watched_content = relationship(
        "Content",
        secondary=user_content_association,
        back_populates="watched_by"
    )

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    content_type = Column(String)  # movie or series
    genre = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with users through watch history
    watched_by = relationship(
        "User",
        secondary=user_content_association,
        back_populates="watched_content"
    ) 