from pathlib import Path
from urllib.parse import quote
import requests


def normalize_public_key(public_url: str) -> str:
    """Превращает ID в полноценную ссылку, если нужно."""
    if not public_url.startswith("http"):
        return f"https://disk.yandex.ru/d/{public_url}"
    return public_url


def get_cache_path(public_key: str, subfolder_path: str) -> Path:
    pubkey_part = public_key.rstrip("/").split("/")[-1]
    subpath_part = subfolder_path.strip("/")#.replace("/", "__")
    return Path(f"src/yandex_image_getter/cache/{pubkey_part}/{subpath_part}/names.txt")


def get_download_url(public_url: str, subfolder_path: str, filename: str) -> str:
    public_key = normalize_public_key(public_url)
    full_path = f"{subfolder_path}/{filename}"
    path_encoded = quote(full_path)
    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
    url = f"{base_url}?public_key={public_key}&path={path_encoded}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["href"]