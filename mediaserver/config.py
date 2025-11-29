from pathlib import Path


# Centralized configuration values.
# Edit the values below to configure your app. No environment variables are used.

# Path to your media root. Example: Path("/Users/you/Media")
BASE_DIR = Path("~/Desktop/media").expanduser().resolve()

# Path to the users JSON file (username: password). Edit as needed.
USERS_FILE = Path("./users.json").resolve()

# API keys: leave empty or paste your keys directly here.
# Note: storing secrets in source is not recommended for production.
TMDB_API_KEY = ""  # e.g. "abcd1234"
TVDB_API_KEY = ""

# Flask secret for sessions
FLASK_SECRET = "dev-secret-change-me"

# Port the app will listen on
PORT = 5000

# Streaming/transcoding settings
USE_FFMPEG_STREAMING = True  # Set False to fallback to plain file streaming
FFMPEG_BIN = "ffmpeg"
FFMPEG_MAX_HEIGHT = 720  # Limit height to reduce bandwidth (keeps aspect ratio)
FFMPEG_VIDEO_BITRATE = "3500k"
FFMPEG_AUDIO_BITRATE = "128k"
FFMPEG_PRESET = "veryfast"
FFMPEG_CHUNK_SIZE = 64 * 1024


def apply_to_app(app):
    """Apply these config values into a Flask `app.config` mapping.

    This keeps the rest of the codebase reading from `current_app.config`.
    """
    app.config["BASE_DIR"] = BASE_DIR
    app.config["USERS_FILE"] = USERS_FILE
    app.config["TMDB_API_KEY"] = TMDB_API_KEY
    app.config["TVDB_API_KEY"] = TVDB_API_KEY
    app.config["FLASK_SECRET"] = FLASK_SECRET
    app.config["PORT"] = PORT
    app.config["USE_FFMPEG_STREAMING"] = USE_FFMPEG_STREAMING
    app.config["FFMPEG_BIN"] = FFMPEG_BIN
    app.config["FFMPEG_MAX_HEIGHT"] = FFMPEG_MAX_HEIGHT
    app.config["FFMPEG_VIDEO_BITRATE"] = FFMPEG_VIDEO_BITRATE
    app.config["FFMPEG_AUDIO_BITRATE"] = FFMPEG_AUDIO_BITRATE
    app.config["FFMPEG_PRESET"] = FFMPEG_PRESET
    app.config["FFMPEG_CHUNK_SIZE"] = FFMPEG_CHUNK_SIZE
