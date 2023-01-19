from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from tmdbv3api import TMDb, Movie, TV

load_dotenv()

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


def search_movie_poster(name):
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    movie = Movie()
    search = movie.search(name)

    if len(search) > 0:
        return {
            "data": [
                {
                    "name": result.title,
                    "poster": "https://image.tmdb.org/t/p/original"
                    + result.poster_path,
                    "release_date": result.release_date,
                }
                for result in search
                if result.poster_path is not None
            ]
        }
    else:
        return {"data": []}


def search_tv_poster(name):
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tv = TV()
    search = tv.search(name)

    if len(search) > 0:
        return {
            "data": [
                {
                    "name": result.name,
                    "poster": "https://image.tmdb.org/t/p/original"
                    + result.poster_path,
                    "first_air_date": result.first_air_date,
                }
                for result in search
                if result.poster_path is not None
            ]
        }
    else:
        return {"data": []}


app = Flask(__name__)

cors = CORS(
    app,
    resources={r"*": {"origins": ["*"]}},
)


@app.route("/")
def hello_world():
    return {
  "message": "working!",
  "For movie posters": "https://posters.niweera.gq/movie/top+gun",
  "For tv show posters": "https://posters.niweera.gq/tv/breaking+bad"
}, 200


@app.route("/movie/<name>")
def get_movie_poster(name):
    results = search_movie_poster(name)
    return results, 200


@app.route("/tv/<name>")
def get_tv_poster(name):
    results = search_tv_poster(name)
    return results, 200


if __name__ == "__main__":
    app.run()
