from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    genres = Column(String)  # Matches init_db.py

    # Relationship to ratings
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=False)
    rating = Column(Float, nullable=False)

    # Relationship back to movie
    movie = relationship("Movie", back_populates="ratings")
