from core.clients.tmdb import TMDBClient


def get_popular_movies():
    tmdb_client = TMDBClient()
    return tmdb_client.get_popular_movies()
