from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.db import Base 
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String)
    year = Column(Integer)
    description = Column(Text)

    # Bidirectional relationship between Movie and Rating models
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True) 
    user_id = Column(Integer)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    rating = Column(Float)

    # Bidirectional relationship between Movie and Rating models
    movie = relationship("Movie", back_populates="ratings") 