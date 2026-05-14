from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database import Base, engine, get_db
from app.models import Movie


# --- Criação das tabelas ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# --- App ---

app = FastAPI(
    title="Movie Catalog API",
    description="API para gerenciar um catálogo de filmes",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Schemas ---

class MovieIn(BaseModel):
    title: str
    director: str
    genre: str
    year: int = Field(..., ge=1888, le=2100)
    rating: float | None = Field(default=None, ge=0.0, le=10.0)


class MovieOut(BaseModel):
    id: int
    title: str
    director: str
    genre: str
    year: int
    rating: float | None

    model_config = {"from_attributes": True}


# --- Rotas ---

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/movies", response_model=MovieOut, status_code=status.HTTP_201_CREATED, tags=["Movies"])
def add_movie(payload: MovieIn, db: Session = Depends(get_db)):
    """Adiciona um novo filme ao catálogo."""
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@app.get("/movies", response_model=list[MovieOut], tags=["Movies"])
def list_movies(genre: str | None = None, db: Session = Depends(get_db)):
    """Lista todos os filmes. Filtra por gênero se informado."""
    query = db.query(Movie)
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    return query.order_by(Movie.created_at.desc()).all()


@app.get("/movies/{movie_id}", response_model=MovieOut, tags=["Movies"])
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Busca um filme pelo ID."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")
    return movie


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Movies"])
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Remove um filme do catálogo."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")
    db.delete(movie)
    db.commit()
