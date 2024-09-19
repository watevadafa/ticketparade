import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class TMDBClient:
    def __init__(self):
        self.bearer_token = f"Bearer {settings.TMDB_BEARER_TOKEN}"
        self.base_url = settings.TMDB_BASE_URL
        self.headers: dict = {
            "accept": "application/json",
            "Authorization": self.bearer_token,
        }

    def authenticate(self):
        url = self.base_url + "/authentication"

        try:
            response = requests.get(url, headers=self.headers)
            is_success = response.json().get("success")

            logger.info(f"Authenticating with TheMovieDB : {is_success}")
            return is_success

        except Exception as e:
            logger.error(f"Error authenticating with TheMovieDB: {e}")

            return False

    def get_popular_movies(self):
        url = self.base_url + "/movie/popular"

        try:
            response = requests.get(url, headers=self.headers)
            return response.json()

        except Exception as e:
            logger.error(f"Error getting popular movies: {e}")
            return None
