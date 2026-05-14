from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
