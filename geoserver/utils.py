import re


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
