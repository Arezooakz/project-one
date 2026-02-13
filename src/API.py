import requests

OMDB_BASE_URL = "http://www.omdbapi.com"


API_KEY = "9c39bffe"
#------------------------------
def omdb_search(query, page=1):
    r = requests.get(
        OMDB_BASE_URL,
        params={"apikey": API_KEY, "s": query, "page": page},
        timeout=20
    )
    r.raise_for_status()
    return r.json()
#------------------------------
def omdb_get_by_imdb_id(imdb_id):
    r = requests.get(
        OMDB_BASE_URL,
        params={"apikey": API_KEY, "i": imdb_id, "plot": "full"},
        timeout=20
    )
    r.raise_for_status()
    return r.json()
#------------------------------
def to_int(x):
    try:
        return int(str(x).strip())
    except:
        return None
#------------------------------
def to_float(x):
    try:
        x = str(x).strip()
        if x == "N/A":
            return None
        return float(x)
    except:
        return None
#------------------------------
def normalize_omdb_movie(detail):
    title = detail.get("Title")
    year = to_int(detail.get("Year"))
    genre = detail.get("Genre") or "Unknown"
    director = detail.get("Director")
    imdb_id = detail.get("imdbID")
    imdb_rating = to_float(detail.get("imdbRating"))
    plot = detail.get("Plot")
    poster = detail.get("Poster")
    actors = detail.get("Actors")

    actor_numbers = None
    if actors and actors != "N/A":
        actor_numbers = len([a.strip() for a in actors.split(",") if a.strip()])

    if poster == "N/A":
        poster = None

    return {
        "movie_name": title,
        "release_year": year,
        "actor_numbers": actor_numbers,
        "budget": None,
        "genre": genre,
        "director": director,
        "imdb_id": imdb_id,
        "imdb_rating": imdb_rating,
        "plot": plot,
        "poster": poster,
    }
