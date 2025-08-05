import os
import requests
import random
from urllib.parse import quote
from pathlib import Path

from .utils import normalize_public_key, get_cache_path, get_download_url


def ensure_names_cache(public_url: str, subfolder_path: str) -> list[str]:
    public_key = normalize_public_key(public_url)
    cache_file = get_cache_path(public_key, subfolder_path)
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8").splitlines()
    else:
        return download_and_cache_names(public_key, subfolder_path, cache_file)


def download_and_cache_names(public_key: str, subfolder_path: str, cache_file: Path) -> list[str]:
    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    path_encoded = quote(subfolder_path)

    names = []
    offset = 0
    limit = 1000

    while True:
        print(f"Получение имени файлов: {len(names)} получено...")
        url = f"{base_url}?public_key={public_key}&path={path_encoded}&limit={limit}&offset={offset}"
        response = requests.get(url)
        if response.status_code == 404:
            raise FileNotFoundError(f"Путь не найден: {subfolder_path}")
        response.raise_for_status()
        data = response.json()
        items = data['_embedded']['items']
        names.extend([item['name'] for item in items if item['type'] == 'file'])

        offset += limit
        if offset >= data['_embedded']['total']:
            break

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text("\n".join(names), encoding="utf-8")
    return names


def download_file_from_url(file_url: str, save_path: str):
    if os.path.exists(save_path):
        print(f"Файл {save_path} уже существует!")
        return
    img_data = requests.get(file_url).content
    with open(save_path, 'wb') as f:
        f.write(img_data)


def download_n_random_images(public_url: str, subfolder_path: str, output_dir: str, n: int, seed: int = 42):
    os.makedirs(output_dir, exist_ok=True)
    names = ensure_names_cache(public_url, subfolder_path)
    rng = random.Random(seed)
    selected_names = rng.sample(names, min(n, len(names)))
    download_images_by_names(public_url, subfolder_path, output_dir, selected_names)


def download_images_by_names(public_url: str, subfolder_path: str, output_dir: str, names: list[str]):
    os.makedirs(output_dir, exist_ok=True)
    for name in names:
        try:
            print(f"Скачиваю: {name}")
            url = get_download_url(public_url, subfolder_path, name)
            download_file_from_url(url, os.path.join(output_dir, name))
        except Exception as e:
            print(f"Ошибка при скачивании {name}: {e}")



if __name__ == "__main__":
    public_url = "https://disk.yandex.ru/d/wDp0Y3_KQ1Rlgw"
    print('Вариант скачивания №1 — Отдельные снимки/03_part_dataset_human_rescue/03_part_dataset_human_rescue1/images')
    ensure_names_cache(
        public_url=public_url,
        subfolder_path='/Вариант скачивания №1 — Отдельные снимки/03_part_dataset_human_rescue/03_part_dataset_human_rescue1/images'
    )
    print('Вариант скачивания №1 — Отдельные снимки/03_part_dataset_human_rescue/03_part_dataset_human_rescue2/images')
    ensure_names_cache(
        public_url=public_url,
        subfolder_path='/Вариант скачивания №1 — Отдельные снимки/03_part_dataset_human_rescue/03_part_dataset_human_rescue2/images'
    )
    print('Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue/images')
    ensure_names_cache(
        public_url=public_url,
        subfolder_path='/Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue/images'
    )
    for i in list(map(lambda x: f"{x:02}", range(1, 16))) + ['19', '35']:
        print(f'Вариант скачивания №1 — Отдельные снимки/01_part_dataset_human_rescue/images/{i}')
        ensure_names_cache(
            public_url=public_url,
            subfolder_path=f'/Вариант скачивания №1 — Отдельные снимки/01_part_dataset_human_rescue/images/{i}'
        )
