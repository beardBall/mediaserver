# Simple Flask Media Server

This repository contains a small Flask-based media server which:

- Uses a JSON file (`users.json`) for simple username/password authentication (plaintext in this example).
- Lists directories under a base media directory (`BASE_MEDIA_DIR`).
- Provides a range-capable streaming endpoint so HTML5 video can play and seek.
- Attempts to fetch metadata from TMDB (The Movie Database) if `TMDB_API_KEY` is provided. The structure allows adding TVDB support if you provide credentials.

Files created:

- `app.py` – main Flask application
- `templates/` – Jinja2 templates for UI
- `users.json` – sample users file
- `requirements.txt` – Python dependencies

Quick start

1. Create a Python virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Prepare a media directory. The app default is `./media` relative to the repo root. Create this structure:

```
./media/Movies
./media/TV Shows
./media/Music
./media/Music videos
```

Place some MP4 files in the folders for testing.

3. Configure environment variables (optional):

- `BASE_MEDIA_DIR` – path to your media directory (defaults to `./media`)
- `USERS_FILE` – path to username/password JSON (defaults to `./users.json`)
- `FLASK_SECRET` – Flask session secret
- `TMDB_API_KEY` – (optional) TMDB API key to fetch metadata

Example to run locally:

```bash
export BASE_MEDIA_DIR=~/Media
export TMDB_API_KEY=your_tmdb_api_key_here
export FLASK_SECRET=replace-with-a-secret
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser. Use the sample credentials in `users.json` (change them before using on a network!).

Notes and next steps

- Passwords are stored in plaintext in `users.json` for the example; switch to hashed passwords (bcrypt) for production.
- The app currently queries TMDB. If you specifically want TheTVDB (TVDB) support, provide API credentials and I can add a provider implementation.
- This is a minimal example — consider using a production WSGI server (gunicorn), HTTPS, reverse proxy, and access controls for deployment.
# mediaserver
My own media server
