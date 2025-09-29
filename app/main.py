from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import joblib
import os
import app.schemas as schemas
from recommender.train_model import train_model
from app.db import get_db, init_db
from app.models import Movie, Rating

app = FastAPI()

movie_titles = []

def reload_model():

    try:
        if os.path.exists("model.pkl"):
            global pivot, similarity, movie_titles
            pivot, similarity, movie_titles = joblib.load("model.pkl")
            print("Model Reloaded Successfully!")
        else:
            print("model.pkl file not found!")

    except Exception as e:
        print(f"Error while loading model: {e}")

@app.on_event("startup")
async def on_startup():
    await init_db()
    if not os.path.exists("model.pkl"):
        print("⚠️ model.pkl not found — training a fresh model...")
        await train_model()
    reload_model()



@app.get("/", tags=["Root"])
def root():
    return {"message" : "Movie Recommender API using FastAPI"}

@app.get("/movies/", tags=["Movies"])
async def get_movies(db: AsyncSession = Depends(get_db)):
    # It uses the SQL SELECT query to fetch all the movie details
    result = await db.execute(select(Movie))    
    return result.scalars().all()

@app.get("/movies/{movie_id}", tags=["Movies"])
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    # Retrieve movie by id
    result = await db.execute(select(Movie).where(Movie.movie_id == movie_id))
    # Retrieve single movie if found otherwise None
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/rate/", tags=["Rating"])
async def add_rating(rating: schemas.RatingCreate, db: AsyncSession = Depends(get_db)):
    new_rating = Rating(**rating.dict())
    db.add(new_rating)
    await db.commit()

    # Model is Retrained after adding new movies
    await train_model()
    # The newly trained model is reloaded into memory
    reload_model()
    return {"message": "Rating added and Model Retrained!"}

@app.get("/recommend/{movie}", tags=["Recommendation"])
def recommend(movie: str, top_n: int = 3):      #top_n = No. of recommendations of movies
    
    actual_movie = None
    for title in movie_titles:
        if title.lower() == movie.lower():
            actual_movie = title
            break

    if actual_movie not in movie_titles:
        raise HTTPException(status_code=404, detail="Movie not in model.")
    
    # Get the index of the movie from movie_titles
    idx = movie_titles.index(actual_movie)

    # Retrieve the similarity scores from the similarity matrix
    sim_scores = list(enumerate(similarity[idx]))

    # sorting similarity scores in descending order except the first one which we gave for recommendation
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    # Extracts the movie_titles from sorted similarity scores
    recs = [movie_titles[i] for i, _ in sim_scores]
    return {"input": actual_movie, "recommendations": recs}

@app.post("/movies/",tags=["Movies"])
async def add_movie(movie: schemas.MovieSchema, db: AsyncSession = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    await db.commit()
    await train_model()
    reload_model()
    return {"message": "Movie Added!"}

@app.delete("/movies/{movie_id}", tags=["Movies"])
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not Found!")
    db.delete(movie)
    await db.commit()
    await train_model()
    reload_model()
    return {"message": "Movie Deleted!"}