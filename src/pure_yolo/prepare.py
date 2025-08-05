from pathlib import Path
from sklearn.model_selection import train_test_split

from yandex_image_getter.download import download_file_from_url
from yandex_image_getter.utils import get_download_url
from .config import YOLO_DATASET_DIR, YOLO_DATA_YAML


def prepare_yolo_dataset(public_url: str, subfolder_path: str, image_names: list[str], val_size=0.2):
    """
    Скачивает изображения и разметку, сохраняет в формате, подходящем для Ultralytics YOLO.
    """
    YOLO_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    train_names, val_names = train_test_split(image_names, test_size=val_size, random_state=42)

    for split, names in [("train", train_names), ("val", val_names)]:
        for kind in ["images", "labels"]:
            path = YOLO_DATASET_DIR / kind / split
            path.mkdir(parents=True, exist_ok=True)

        for name in names:
            img_url = get_download_url(public_url, f"{subfolder_path}/images", name)
            img_path = YOLO_DATASET_DIR / "images" / split / name
            download_file_from_url(img_url, str(img_path))

            label_name = name.replace(".jpg", ".txt")
            label_url = get_download_url(public_url, f"{subfolder_path}/labels", label_name)
            label_path = YOLO_DATASET_DIR / "labels" / split / label_name
            download_file_from_url(label_url, str(label_path))

    generate_yaml_config()


def generate_yaml_config():
    yaml_content = f"""path: {YOLO_DATASET_DIR}
train: images/train
val: images/val
nc: 1
names: ['human']
"""
    YOLO_DATA_YAML.write_text(yaml_content, encoding="utf-8")
