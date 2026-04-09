from __future__ import annotations

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_from_root(path: str | Path, root: Path | None = None) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    base_root = root or get_project_root()
    return (base_root / candidate).resolve()


def to_project_relative_path(path: str | Path, root: Path | None = None) -> str:
    resolved_path = resolve_from_root(path, root)
    base_root = root or get_project_root()
    try:
        return resolved_path.relative_to(base_root).as_posix()
    except ValueError:
        return resolved_path.as_posix()


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
