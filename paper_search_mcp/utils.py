import re

def extract_doi(text: str) -> str:
    """Extract DOI from arbitrary text or URL if present."""
    if not text:
        return ""
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.IGNORECASE)
    return match.group(0).rstrip(".,;)") if match else ""


def url_host_matches(url_text: str, host: str) -> bool:
    """Return True when ``url_text`` is a URL whose host is ``host`` or a subdomain of it.

    Parses the URL instead of doing substring matching, so a host like
    ``notdoi.org.evil.example`` or ``https://evil.example/?q=doi.org`` is not
    mistaken for ``doi.org``.
    """
    from urllib.parse import urlparse

    candidate = url_text.strip()
    if not candidate:
        return False
    try:
        parsed = urlparse(candidate)
        host_found = parsed.hostname
        if not host_found and "//" not in candidate:
            # schemeless form like "doi.org/10.1000/x"
            host_found = urlparse("//" + candidate).hostname
    except ValueError:
        return False
    if not host_found:
        return False
    url_host = host_found.lower()
    host = host.lower()
    return url_host == host or url_host.endswith("." + host)


def doi_from_url(url_text: str) -> str:
    """Return the DOI path from a doi.org URL, or an empty string."""
    from urllib.parse import urlparse

    candidate = url_text.strip()
    if not url_host_matches(candidate, "doi.org"):
        return ""
    if "://" not in candidate:
        parsed = urlparse("//" + candidate)
    else:
        parsed = urlparse(candidate)
    return parsed.path.lstrip("/")
