import re
import zipfile
from pathlib import Path
from typing import IO, Union


def clean_html(content: str) -> str:
    content = re.sub(r"&#39;", "'", content).strip()
    return re.sub(r"&#47;", "/", content).strip()


def is_html(content: str) -> bool:
    return content.strip().lower().startswith("<!doctype html>")


def find_html_body(content: str) -> str:
    body = re.search(r"<body>(.*?)</body>", content, re.DOTALL)
    return body.group(1) if body else ""


def find_html_message_section(content: str) -> str:
    match = re.search(r"<p><b>Message</b>(.*?)</p>", content, re.DOTALL)
    msg = match.group(1) if match else ""
    return clean_html(msg)


def find_html_description_section(content: str) -> str:
    match = re.search(r"<p><b>Description</b>(.*?)</p>", content, re.DOTALL)
    msg = match.group(1) if match else ""
    return clean_html(msg)


def is_zip(file: Union[str, Path, IO[bytes]]) -> bool:
    """Checks whether a path or a file object is a ZIP archive, leaving the read position of a file object unchanged."""
    if isinstance(file, (str, Path)):
        return zipfile.is_zipfile(file)
    position = file.tell()
    try:
        return zipfile.is_zipfile(file)
    finally:
        file.seek(position)


def file_name(file: Union[str, Path, IO[bytes]]) -> Union[str, None]:
    """Returns the name of a path, or of a file object opened from a path (``open(path, "rb")``)."""
    name = file if isinstance(file, (str, Path)) else getattr(file, "name", None)
    return Path(name).name if isinstance(name, (str, Path)) else None
