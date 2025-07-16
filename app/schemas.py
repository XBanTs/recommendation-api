from pydantic import BaseModel

class MovieSchema(BaseModel):
    movie_id: int
    title: str
    genre: str
    year: int
    description: str

    class Config:
        orm_mode = True
 
class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float