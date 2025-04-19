# Netflix-like Recommendation System

This project implements a content recommendation system similar to Netflix, using FastAPI, PostgreSQL, and KMeans clustering for personalized recommendations.

## Features

- User management
- Content management
- Watch history tracking
- Personalized content recommendations using KMeans clustering
- REST API endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database:
   - Create a new database named `netflix_recommender`
   - Update the DATABASE_URL in `.env` file (or use the default)

5. Initialize the database:
   ```bash
   python -m app.init_db
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /users/` - Create a new user
- `POST /content/` - Add new content
- `POST /users/{user_id}/watch/{content_id}` - Mark content as watched
- `GET /users/{user_id}/recommendations` - Get personalized recommendations

## Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## How it Works

1. The system uses KMeans clustering to group similar content based on features like:
   - Genre
   - Rating
   - Release year

2. When a user watches content, their preferences are tracked in the database.

3. The recommendation system:
   - Analyzes the user's watch history
   - Identifies the user's preferred content cluster
   - Recommends similar content from the same cluster
   - Filters out already watched content
   - Sorts recommendations by rating

## Contributing

Feel free to submit issues and enhancement requests. 