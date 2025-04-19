from sqlalchemy.orm import Session
from . import models, database
from .database import engine

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = Session(bind=engine)
    
    try:
        # Create sample users
        users = [
            models.User(username="user1", email="user1@example.com", hashed_password="password1"),
            models.User(username="user2", email="user2@example.com", hashed_password="password2"),
        ]
        
        for user in users:
            db.add(user)
        
        # Create sample content
        contents = [
            models.Content(
                title="The Matrix",
                description="A computer hacker learns about the true nature of reality",
                content_type="movie",
                genre="Action,Sci-Fi",
                release_year=1999,
                rating=8.7
            ),
            models.Content(
                title="Inception",
                description="A thief who steals corporate secrets through dream-sharing technology",
                content_type="movie",
                genre="Action,Sci-Fi,Thriller",
                release_year=2010,
                rating=8.8
            ),
            models.Content(
                title="Breaking Bad",
                description="A high school chemistry teacher turned methamphetamine manufacturer",
                content_type="series",
                genre="Drama,Crime,Thriller",
                release_year=2008,
                rating=9.5
            ),
            models.Content(
                title="Stranger Things",
                description="When a young boy vanishes, a small town uncovers a mystery",
                content_type="series",
                genre="Drama,Fantasy,Horror",
                release_year=2016,
                rating=8.7
            ),
        ]
        
        for content in contents:
            db.add(content)
        
        db.commit()
        
        # Add some watch history
        user1 = db.query(models.User).filter(models.User.username == "user1").first()
        matrix = db.query(models.Content).filter(models.Content.title == "The Matrix").first()
        inception = db.query(models.Content).filter(models.Content.title == "Inception").first()
        
        user1.watched_content.append(matrix)
        user1.watched_content.append(inception)
        
        db.commit()
        
        print("Database initialized with sample data!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 