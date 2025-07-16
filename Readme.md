# Movie Recommender API

A FastAPI-based movie recommendation system that uses collaborative filtering to suggest movies based on user preferences. The system automatically retrains the machine learning model when new movies or ratings are added.

## Features

- **Movie Management**: Add, retrieve, and delete movies from the database
- **Rating System**: Users can rate movies to improve recommendations
- **Smart Recommendations**: Get personalized movie recommendations using collaborative filtering
- **Auto-Retraining**: Model automatically retrains when new data is added
- **Async Support**: Built with FastAPI for high performance

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM with async support
- **Scikit-learn**: Machine learning library for recommendation algorithms
- **Joblib**: Model serialization and loading
- **PostgreSQL/SQLite**: Database support (configurable)

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation(Swagger UI).

## API Endpoints

### Root
- **GET** `/` - Welcome message and API info

### Movies
- **GET** `/movies/` - Get all movies
- **GET** `/movies/{movie_id}` - Get a specific movie by ID
- **POST** `/movies/` - Add a new movie
- **DELETE** `/movies/{movie_id}` - Delete a movie by ID

### Ratings
- **POST** `/rate/` - Add a movie rating

### Recommendations
- **GET** `/recommend/{movie}?top_n={number}` - Get movie recommendations

## Usage Examples

### Get All Movies
```bash
curl -X GET "http://localhost:8000/movies/"
```

## How It Works

1. **Data Storage**: Movies and ratings are stored in a relational database
2. **Model Training**: The system uses collaborative filtering to build a similarity matrix
3. **Recommendations**: When a movie is requested, the system finds similar movies using cosine similarity
4. **Auto-Retraining**: The model retrains automatically when new movies or ratings are added
5. **Caching**: Trained models are cached using joblib for fast predictions

> [!NOTE]
> I have used the PostgreSQL Database for Model training and User ratings.  You can also use CSVs for your preferences to train the model.
