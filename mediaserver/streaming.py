from flask import Response
from .utils import get_range


def stream_file(req, base, relpath):
    target = base.joinpath(relpath).resolve()
    if not target.exists() or not target.is_file():
        return None
    file_size = target.stat().st_size
    start, end = get_range(req, file_size)

    if start >= file_size:
        return Response(status=416)

    length = end - start + 1
    with open(target, "rb") as f:
        f.seek(start)
        data = f.read(length)

    rv = Response(data, 206 if req.headers.get("Range") else 200, mimetype="video/mp4")
    rv.headers.add("Content-Range", f"bytes {start}-{end}/{file_size}")
    rv.headers.add("Accept-Ranges", "bytes")
    rv.headers.add("Content-Length", str(length))
    return rv
