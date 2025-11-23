from flask import Blueprint, current_app, render_template, request, redirect, url_for, abort
from .auth import load_users, login_required
from .utils import safe_path_join, guess_title
from .metadata import fetch_metadata_tmdb
from .streaming import stream_file
from urllib.parse import quote
from pathlib import Path

bp = Blueprint("main", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        users = load_users()
        if username in users and users[username] == password:
            from flask import session

            session["user"] = username
            next_url = request.args.get("next") or url_for("main.index")
            return redirect(next_url)
        error = "Invalid username or password"
    return render_template("login.html", error=error)


@bp.route("/logout")
def logout():
    from flask import session

    session.pop("user", None)
    return redirect(url_for("main.login"))


@bp.route("/")
@login_required
def index():
    base = current_app.config.get("BASE_DIR")
    items = []
    if not base.exists():
        return render_template("index.html", base_exists=False, base_dir=str(base))
    for child in sorted(base.iterdir()):
        if child.is_dir():
            items.append({"name": child.name, "path": quote(child.relative_to(base).as_posix())})
    return render_template("index.html", base_exists=True, categories=items)


@bp.route("/browse/<path:subpath>")
@login_required
def browse(subpath):
    base = current_app.config.get("BASE_DIR")
    try:
        target = safe_path_join(base, subpath)
    except Exception:
        abort(404)
    if not target.exists():
        abort(404)
    entries = []
    for p in sorted(target.iterdir()):
        rel = p.relative_to(base)
        if p.is_dir():
            entries.append({"type": "dir", "name": p.name, "path": quote(rel.as_posix())})
        else:
            entries.append({"type": "file", "name": p.name, "path": quote(rel.as_posix())})
    parent = None
    if target != base:
        parent = quote(target.parent.relative_to(base).as_posix())
    return render_template("listing.html", entries=entries, parent=parent, current=quote(Path(subpath).as_posix()))


@bp.route("/metadata/<path:relpath>")
@login_required
def metadata(relpath):
    base = current_app.config.get("BASE_DIR")
    try:
        target = safe_path_join(base, relpath)
    except Exception:
        abort(404)
    if not target.exists() or target.is_dir():
        abort(404)
    title = guess_title(target.name)
    meta = fetch_metadata_tmdb(title)
    return render_template("metadata.html", meta=meta, filename=target.name, title=title)


@bp.route("/player/<path:relpath>")
@login_required
def player(relpath):
    base = current_app.config.get("BASE_DIR")
    try:
        target = safe_path_join(base, relpath)
    except Exception:
        abort(404)
    if not target.exists() or not target.is_file():
        abort(404)
    return render_template("player.html", filename=target.relative_to(base).as_posix())


@bp.route("/stream/<path:relpath>")
@login_required
def stream(relpath):
    base = current_app.config.get("BASE_DIR")
    try:
        # check safety first
        _ = safe_path_join(base, relpath)
    except Exception:
        abort(404)
    rv = stream_file(request, base, relpath)
    if rv is None:
        abort(404)
    return rv
