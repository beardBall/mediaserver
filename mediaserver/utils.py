import re
from pathlib import Path
from flask import current_app


def safe_path_join(base: Path, *paths) -> Path:
    candidate = base.joinpath(*paths).resolve()
    if base not in candidate.parents and candidate != base:
        raise ValueError("Path escaped base directory")
    return candidate


def guess_title(fname: str) -> str:
    name = Path(fname).stem
    name = re.sub(r"[._]+", " ", name)
    name = re.sub(r"\b(19|20)\d{2}\b", "", name)
    name = re.sub(r"\b(1080p|720p|2160p|x264|x265|h264|h265|bluray|web[-.]dl|hdrip)\b", "", name, flags=re.I)
    return name.strip()


def get_range(request, file_size):
    range_header = request.headers.get("Range", None)
    if not range_header:
        return 0, file_size - 1
    m = re.match(r"bytes=(\d+)-(\d*)", range_header)
    if m:
        start = int(m.group(1))
        end = m.group(2)
        end = int(end) if end else file_size - 1
        return start, end
    return 0, file_size - 1
