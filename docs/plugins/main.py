from __future__ import annotations as _annotations

import logging
import re
from pathlib import Path

from mkdocs.config import Config

logger = logging.getLogger("mkdocs.plugin")
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


def on_pre_build(config: Config) -> None:
    add_changelog()
    add_notebooks()


def add_changelog() -> None:
    file_path = PROJECT_ROOT / "CHANGELOG.md"
    changelog = file_path.read_text(encoding="utf-8")

    # Regex to find the "Unreleased" section and exclude it from the output
    pattern = r"## Unreleased.*?(?=## \d|\Z)"
    changelog = re.sub(pattern, "", changelog, flags=re.DOTALL)
    # Strip and remove extra lines
    changelog = re.sub(r"\n{3,}", "\n\n", changelog.strip() + "\n")

    # Write the filtered content to a new file in the docs directory
    # Avoid writing file unless the content has changed to avoid infinite build loop
    out_path = DOCS_DIR / "changelog.md"
    if not out_path.is_file() or out_path.read_text(encoding="utf-8") != changelog:
        out_path.write_text(changelog, encoding="utf-8")


def add_notebooks() -> None:
    # Remove all notebooks that are no longer in the notebooks directory
    for notebook_path in DOCS_DIR.glob("notebooks/*.ipynb"):
        if not (PROJECT_ROOT / "notebooks" / notebook_path.name).is_file():
            notebook_path.unlink()

    # Copy all notebooks from the notebooks directory to the docs directory
    for notebook_path in Path(PROJECT_ROOT, "notebooks").glob("*.ipynb"):
        out_path = DOCS_DIR / "notebooks" / notebook_path.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if not out_path.is_file() or out_path.read_text(encoding="utf-8") != notebook_path.read_text(encoding="utf-8"):
            out_path.write_text(notebook_path.read_text(encoding="utf-8"), encoding="utf-8")
