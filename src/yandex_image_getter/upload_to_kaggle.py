import os
import json
import subprocess

DATASET_DIR = "src/yandex_image_getter/saved/wDp0Y3_KQ1Rlgw/Вариант скачивания №1 — Отдельные снимки"
DATASET_ID = "chickowar/archipelag-hackathon-dataset-2025"

# Шаг 1: Создаём metadata
metadata = {
    "title": "My Big Image Dataset",
    "id": DATASET_ID,
    "licenses": [{"name": "CC0-1.0"}]
}

with open(os.path.join(DATASET_DIR, "dataset-metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)

# Шаг 2: Загружаем
subprocess.run([
    "kaggle", "datasets", "create",
    "-p", DATASET_DIR,
    "--dir-mode", "zip"
])

