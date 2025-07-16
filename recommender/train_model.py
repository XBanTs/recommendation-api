import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import asyncio
from app.models import Rating,Movie
from app.db import AsyncSessionLocal
from sqlalchemy import select, join


# movies_df = pd.read_csv("movies.csv")
# ratings_df = pd.read_csv("ratings.csv")

# merged_df = ratings_df.merge(movies_df, on="movie_id")

# pivot = merged_df.pivot_table(index='user_id', columns='title', values='rating')

# pivot_filled = pivot.fillna(0)

# similarity = cosine_similarity(pivot_filled.T)

# movie_titles = list(pivot.columns)

# joblib.dump((pivot, similarity, movie_titles), "model.pkl") 

# print("✅ model.pkl file created successfully from CSV data.")

async def train_model():
    async with AsyncSessionLocal() as session:

        # use SELECT query to select user_id, rating and title from Movies table
        query = select(
            Rating.user_id,
            Rating.rating,
            Movie.title
        ).select_from(
            # Merge the movie_id from Ratings and movie_id from Movies table
            join(Rating, Movie, Rating.movie_id == Movie.movie_id)
        )

        result = await session.execute(query)
        rows = result.fetchall()

        # Convert the result to DataFrame
        df = pd.DataFrame(rows, columns=["user_id", "rating", "title"])

        if df.empty:
            print("Not enough data to train the model!")
            return
        # Create pivot table
        pivot = df.pivot_table(index='user_id', columns='title', values='rating').fillna(0)

        # Compute similarity
        similarity = cosine_similarity(pivot.T)

        # Save model
        joblib.dump((pivot, similarity, list(pivot.columns)), "model.pkl")
        print("model.pkl Updated!!!")

if __name__ == "__main__":
    asyncio.run(train_model())



