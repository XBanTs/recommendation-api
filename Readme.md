# Movie Recommender API

A FastAPI-based movie recommendation system that uses collaborative filtering to suggest movies based on user preferences. The system automatically retrains the machine learning model when new movies or ratings are added.

## Features

- **Movie Management**: Add, retrieve, and delete movies from the database
- **Rating System**: Users can rate movies to improve recommendations
- **Smart Recommendations**: Get personalized movie recommendations using collaborative filtering
- **Auto-Retraining**: Model automatically retrains when new data is added
- **RESTful API**: Clean and intuitive API endpoints
- **Async Support**: Built with FastAPI for high performance

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM with async support
- **Scikit-learn**: Machine learning library for recommendation algorithms
- **Joblib**: Model serialization and loading
- **PostgreSQL/SQLite**: Database support (configurable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-recommender-api.git
cd movie-recommender-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your database configuration in the database settings.

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

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

### Get Movie by ID
```bash
curl -X GET "http://localhost:8000/movies/1"
```

### Add a New Movie
```bash
curl -X POST "http://localhost:8000/movies/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Matrix",
    "genre": "Sci-Fi",
    "year": 1999
  }'
```

### Rate a Movie
```bash
curl -X POST "http://localhost:8000/rate/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "movie_id": 1,
    "rating": 5.0
  }'
```

### Get Recommendations
```bash
curl -X GET "http://localhost:8000/recommend/The%20Matrix?top_n=5"
```

### Delete a Movie
```bash
curl -X DELETE "http://localhost:8000/movies/1"
```

## Request/Response Examples

### Movie Recommendation Response
```json
{
  "input": "The Matrix",
  "recommendations": [
    "The Matrix Reloaded",
    "The Matrix Revolutions",
    "Blade Runner",
    "Ghost in the Shell",
    "Minority Report"
  ]
}
```

### Movie Details Response
```json
{
  "movie_id": 1,
  "title": "The Matrix",
  "genre": "Sci-Fi",
  "year": 1999,
  "director": "The Wachowskis"
}
```

## How It Works

1. **Data Storage**: Movies and ratings are stored in a relational database
2. **Model Training**: The system uses collaborative filtering to build a similarity matrix
3. **Recommendations**: When a movie is requested, the system finds similar movies using cosine similarity
4. **Auto-Retraining**: The model retrains automatically when new movies or ratings are added
5. **Caching**: Trained models are cached using joblib for fast predictions

## Model Details

The recommendation system uses:
- **Collaborative Filtering**: Finds patterns in user-movie interactions
- **Cosine Similarity**: Measures similarity between movies based on user ratings
- **Pivot Tables**: Creates user-movie matrices for efficient computation

## Error Handling

The API includes comprehensive error handling:
- **404 Not Found**: When movies or resources don't exist
- **500 Internal Server Error**: For model loading or database issues
- **422 Validation Error**: For invalid request data

## Configuration

Create a `.env` file for environment variables:
```
DATABASE_URL=postgresql://user:password@localhost/moviedb
MODEL_PATH=model.pkl
DEBUG=True
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Enhancements

- [ ] User authentication and authorization
- [ ] More sophisticated recommendation algorithms
- [ ] Movie metadata enrichment (posters, descriptions, etc.)
- [ ] Rating analytics and insights
- [ ] Caching layer for better performance
- [ ] Docker containerization
- [ ] Unit and integration tests

## Support

For support, please open an issue in the GitHub repository or contact [your-email@example.com].

---

**Built with ❤️ using FastAPI**