import os
from pathlib import Path

from flask import Flask


def create_app():
    pkg_root = Path(__file__).resolve().parent
    # templates and static remain in repo root; point Flask there
    templates_dir = str(pkg_root.parent / "templates")
    static_dir = str(pkg_root.parent / "static")

    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    # load config from our centralized module
    from . import config as _config

    app.secret_key = _config.FLASK_SECRET
    _config.apply_to_app(app)

    # register views blueprint
    from .views import bp as main_bp

    app.register_blueprint(main_bp)

    return app
