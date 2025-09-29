# 🎬 Movie Recommendation System

A sophisticated, full-stack movie recommendation application built with **FastAPI** and **Streamlit** that leverages collaborative filtering and machine learning to provide personalized movie recommendations. The system features automatic model retraining, real-time recommendations, and an intuitive web interface.

## ✨ Features

### 🎯 Core Functionality
- **Intelligent Recommendations**: Advanced collaborative filtering using cosine similarity
- **Real-time Rating System**: Users can rate movies to improve recommendation accuracy
- **Auto-Retraining**: ML model automatically retrains when new data is added
- **Movie Management**: Complete CRUD operations for movies
- **Interactive Web UI**: Beautiful Streamlit frontend for easy interaction

### 🚀 Technical Highlights
- **Async FastAPI Backend**: High-performance REST API with automatic documentation
- **SQLAlchemy ORM**: Robust database management with async support
- **Scikit-learn ML**: Professional-grade machine learning algorithms
- **Model Persistence**: Efficient model caching with joblib
- **Database Flexibility**: Supports both PostgreSQL and SQLite

## 🏗️ Architecture

```
Movie-Recommendation-Application/
├── app/                    # FastAPI backend
│   ├── main.py            # API endpoints and business logic
│   ├── models.py          # Database models (Movie, Rating)
│   ├── schemas.py         # Pydantic schemas for validation
│   ├── db.py              # Database configuration
│   └── create_tables.py   # Database initialization
├── frontend/              # Streamlit web interface
│   └── app.py            # Interactive UI for recommendations and ratings
├── recommender/           # Machine learning module
│   └── train_model.py    # Collaborative filtering implementation
├── images/               # Application screenshots
└── requirements.txt      # Python dependencies
```

## 📸 Application Screenshots

### Get Movie Recommendations
![Movie Recommendations Interface](images/movrecommender1.png)
*The recommendation interface allows users to select a movie and get personalized suggestions based on collaborative filtering*

### Rate Movies
![Movie Rating Interface](images/movrecommender2.png)
*Users can rate movies on a scale of 0-5 stars, which automatically retrains the ML model for better recommendations*

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend API** | FastAPI | High-performance async REST API |
| **Frontend** | Streamlit | Interactive web interface |
| **Database** | SQLAlchemy + PostgreSQL/SQLite | Data persistence and ORM |
| **Machine Learning** | Scikit-learn | Collaborative filtering algorithms |
| **Model Storage** | Joblib | Efficient model serialization |
| **Validation** | Pydantic | Request/response validation |

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- PostgreSQL (optional - SQLite works too)

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd Movie-Recommendation-Application

# Create virtual environment (recommended)
python -m venv movie_rec_env
source movie_rec_env/bin/activate  # On Windows: movie_rec_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Initialize the database with sample data
python init_db.py
```

### 3. Start the FastAPI Backend
```bash
# Run the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`
- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`

### 4. Launch the Streamlit Frontend
```bash
# In a new terminal, start the web interface
streamlit run frontend/app.py
```
The web application will open automatically at `http://localhost:8501`

## 📚 API Documentation

### 🎬 Movies Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/movies/` | Retrieve all movies |
| `GET` | `/movies/{movie_id}` | Get specific movie by ID |
| `POST` | `/movies/` | Add a new movie |
| `DELETE` | `/movies/{movie_id}` | Delete a movie |

### ⭐ Ratings Endpoint
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/rate/` | Submit a movie rating (triggers model retraining) |

### 🎯 Recommendations Endpoint
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/recommend/{movie}?top_n={number}` | Get movie recommendations |

### Example API Usage
```bash
# Get recommendations for "Toy Story"
curl "http://localhost:8000/recommend/Toy%20Story?top_n=5"

# Add a rating
curl -X POST "http://localhost:8000/rate/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "movie_id": 1, "rating": 4.5}'
```

## 🧠 How the ML Algorithm Works

### 1. **Data Collection**
- User ratings are stored in a relational database
- Each rating links a user, movie, and score (0-5 stars)

### 2. **Collaborative Filtering**
- Creates a user-movie matrix from rating data
- Uses cosine similarity to find movies with similar rating patterns
- Handles sparse data with zero-filling for unrated movies

### 3. **Recommendation Generation**
- Calculates similarity scores between movies
- Returns top-N most similar movies to the input
- Excludes the input movie from recommendations

### 4. **Automatic Retraining**
- Model retrains whenever new movies or ratings are added
- Ensures recommendations stay current with user preferences
- Uses joblib for efficient model persistence

## 🎮 Using the Application

### Web Interface (Recommended)
1. **Start both servers** (FastAPI + Streamlit)
2. **Open** `http://localhost:8501` in your browser
3. **Get Recommendations**: Select a movie and click "Get Recommendations"
4. **Rate Movies**: Choose a movie, set your rating, and submit

### API Interface
1. **Visit** `http://localhost:8000/docs` for interactive API documentation
2. **Test endpoints** directly in the Swagger UI
3. **Integrate** with your own applications using the REST API

## 🔧 Configuration

### Database Configuration
Edit `app/db.py` to configure your database:
```python
# For PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/moviedb"

# For SQLite (default)
DATABASE_URL = "sqlite+aiosqlite:///./movies.db"
```

### Model Parameters
Adjust recommendation parameters in `app/main.py`:
```python
# Change default number of recommendations
@app.get("/recommend/{movie}")
def recommend(movie: str, top_n: int = 5):  # Default changed to 5
```

## 🐛 Troubleshooting

### Common Issues

**"Model not found" error**
```bash
# Retrain the model manually
python -c "import asyncio; from recommender.train_model import train_model; asyncio.run(train_model())"
```

**Database connection issues**
```bash
# Reinitialize the database
python init_db.py
```

**Port already in use**
```bash
# Use different ports
uvicorn app.main:app --port 8001
streamlit run frontend/app.py --server.port 8502
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent async web framework
- **Streamlit** for making beautiful web apps simple
- **Scikit-learn** for robust machine learning algorithms
- **SQLAlchemy** for powerful database ORM capabilities

---

**Built with ❤️ for movie enthusiasts and ML practitioners**