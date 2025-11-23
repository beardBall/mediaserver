import requests
from flask import current_app


def fetch_metadata_tmdb(query: str):
    tmdb_key = "76d79a20-9e1d-406c-97d9-48318e9ff087"
    # ""current_app.config.get("TMDB_API_KEY")
    if not tmdb_key:
        return None
    params = {"api_key": tmdb_key, "query": query}
    try:
        r = requests.get("https://api.themoviedb.org/3/search/movie", params=params, timeout=6)
        if r.ok:
            data = r.json()
            if data.get("results"):
                item = data["results"][0]
                return {
                    "type": "movie",
                    "title": item.get("title") or query,
                    "overview": item.get("overview"),
                    "poster_path": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None,
                    "tmdb_id": item.get("id"),
                }
        r2 = requests.get("https://api.themoviedb.org/3/search/tv", params=params, timeout=6)
        if r2.ok:
            data = r2.json()
            if data.get("results"):
                item = data["results"][0]
                return {
                    "type": "tv",
                    "title": item.get("name") or query,
                    "overview": item.get("overview"),
                    "poster_path": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None,
                    "tmdb_id": item.get("id"),
                }
    except Exception:
        return None
    return None
