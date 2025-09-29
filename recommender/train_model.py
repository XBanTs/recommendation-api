import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import asyncio
from app.models import Rating, Movie
from app.db import AsyncSessionLocal
from sqlalchemy import select, join, outerjoin


async def train_model():
    async with AsyncSessionLocal() as session:
        # ✅ Get all movies
        movies_result = await session.execute(select(Movie.title))
        movies = [row[0] for row in movies_result.fetchall()]

        # ✅ Get ratings with movie titles (outer join so unrated movies are still included)
        query = select(
            Rating.user_id,
            Rating.rating,
            Movie.title
        ).select_from(
            outerjoin(Rating, Movie, Rating.movie_id == Movie.movie_id)
        )

        result = await session.execute(query)
        rows = result.fetchall()

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=["user_id", "rating", "title"])

        if df.empty:
            print("⚠️ Not enough data to train the model. Creating empty model.pkl")
            joblib.dump((pd.DataFrame(), [], movies), "model.pkl")
            return

        # Create pivot table (user x movie matrix)
        pivot = df.pivot_table(index="user_id", columns="title", values="rating").fillna(0)

        # Ensure all movies exist in pivot (add missing columns with zeros)
        for movie in movies:
            if movie not in pivot.columns:
                pivot[movie] = 0

        # Reorder columns to match movie list
        pivot = pivot[movies]

        # Compute similarity
        similarity = cosine_similarity(pivot.T)

        # Save model with all movies
        joblib.dump((pivot, similarity, movies), "model.pkl")
        print("✅ model.pkl updated with", len(movies), "movies")


if __name__ == "__main__":
    asyncio.run(train_model())
