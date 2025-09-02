from dataclasses import dataclass
import requests
import json
from typing import List, Optional, Protocol
from pydantic import BaseModel
import os
import platform


API_KEY = os.getenv("API_KEY")


class Movie(BaseModel):
    adult: bool
    backdrop_path: Optional[str] = None
    genre_ids: List[int] = []
    id: int
    original_language: str
    original_title: str
    overview: Optional[str] = None
    popularity: float
    poster_path: Optional[str] = None
    release_date: Optional[str] = None
    title: str
    video: bool
    vote_average: float
    vote_count: int


class MovieDB(Protocol):
    def searchMovies(self, query: str) -> List[Movie]: ...


@dataclass
class MovieDBImpl(MovieDB):

    def getMovie(self, id: int) -> Movie:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}")
        data = response.json()
        return Movie(**data)

    def searchMovies(self, query: str) -> List[Movie]:
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"
        headers = {
            'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NzNkMTI5NzI1NzU2ODZmNjBlNGVjZWMzY2JlOTE3OCIsIm5iZiI6MTc1NjUwNjY0MS4xMDMwMDAyLCJzdWIiOiI2OGIyMmExMTNjYWZjOWYxMmI1NGRjMjUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.cM-DM7_Rv56Nhgo7IhRFV9FxPD5LTPrgWdYy5GKsNXo",
            'accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"Error en la API: {response.status_code} - {response.text}")

        data = response.json()

        # Convertir los resultados en una lista de objetos Movie
        movies = [Movie(**m) for m in data.get("results", [])]
        return movies


def clear_console():
    """Limpia la consola según el sistema operativo"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def main():
    db = MovieDBImpl()

    while True:
        query = input("🔍 Escribe el nombre de la película (o 'salir' para terminar): ")
        if query.lower() == "salir":
            print("👋 Hasta luego!")
            break

        try:
            results = db.searchMovies(query)

            if not results:
                print("\n⚠️ No se encontraron resultados.")
            else:
                print("\n🎬 Resultados de búsqueda:\n")
                for i, movie in enumerate(results, start=1):
                    print(f"{i}. {movie.title} ({movie.release_date}) ⭐ {movie.vote_average}")

        except Exception as e:
            print(f"⚠️ Error al buscar películas: {e}")

        input("\nPresiona ENTER para hacer otra búsqueda...")
        clear_console()



if __name__ == "__main__":
    main()
