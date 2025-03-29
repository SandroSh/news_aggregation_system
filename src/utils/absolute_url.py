from urllib.parse import urljoin


def absolute_url(base_url:str,relative_url:str) -> str:
    return urljoin(base_url, relative_url)