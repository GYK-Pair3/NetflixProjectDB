import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from .models import User, Content, user_content_association
import pandas as pd

class ContentRecommender:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.content_features = None
        self.content_clusters = None

    def prepare_content_features(self, db: Session):
        # Get all content
        contents = db.query(Content).all()
        
        # Create feature matrix
        features = []
        content_ids = []
        
        for content in contents:
            # Convert genre string to one-hot encoding
            genres = content.genre.split(',')
            genre_features = {genre: 1 for genre in genres}
            
            # Create feature vector
            feature_vector = [
                content.rating,
                content.release_year,
                *[genre_features.get(genre, 0) for genre in ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Romance']]
            ]
            
            features.append(feature_vector)
            content_ids.append(content.id)
        
        self.content_features = np.array(features)
        self.content_ids = content_ids
        
        # Fit KMeans
        self.content_clusters = self.kmeans.fit_predict(self.content_features)

    def get_user_cluster(self, db: Session, user_id: int):
        # Get user's watched content
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.watched_content:
            return None
            
        # Get average features of watched content
        watched_features = []
        for content in user.watched_content:
            content_idx = self.content_ids.index(content.id)
            watched_features.append(self.content_features[content_idx])
            
        avg_features = np.mean(watched_features, axis=0)
        
        # Predict cluster for user
        user_cluster = self.kmeans.predict([avg_features])[0]
        return user_cluster

    def recommend_content(self, db: Session, user_id: int, n_recommendations=5):
        if self.content_features is None:
            self.prepare_content_features(db)
            
        user_cluster = self.get_user_cluster(db, user_id)
        if user_cluster is None:
            # If user has no watch history, return popular content
            return db.query(Content).order_by(Content.rating.desc()).limit(n_recommendations).all()
            
        # Get content from user's cluster
        cluster_content_indices = np.where(self.content_clusters == user_cluster)[0]
        cluster_content_ids = [self.content_ids[idx] for idx in cluster_content_indices]
        
        # Get user's watched content IDs
        user = db.query(User).filter(User.id == user_id).first()
        watched_content_ids = [content.id for content in user.watched_content]
        
        # Filter out watched content
        recommended_content_ids = [cid for cid in cluster_content_ids if cid not in watched_content_ids]
        
        # Get recommended content
        recommended_content = db.query(Content).filter(Content.id.in_(recommended_content_ids)).all()
        
        # Sort by rating and return top n
        recommended_content.sort(key=lambda x: x.rating, reverse=True)
        return recommended_content[:n_recommendations] 