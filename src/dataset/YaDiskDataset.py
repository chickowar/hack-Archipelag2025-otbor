import os
import torch
from torch import Tensor
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
from pathlib import Path

from yandex_image_getter.download import (
    get_download_url,
    download_file_from_url,
    normalize_public_key
)


class YaDiskDataset(Dataset):
    def __init__(
        self,
        public_url: str,
        subfolder_path: str,
        image_names: list[str],
        transform=None
    ):
        self.public_url = normalize_public_key(public_url)
        self.subfolder_path = subfolder_path#.strip("/")
        self.image_names = image_names
        self.transform = transform or transforms.ToTensor()

        self.cache_root = Path(f"src/yandex_image_getter/cache/{self.public_url.split('/')[-1]}")
        self.saved_root = Path(f"src/yandex_image_getter/saved/{self.public_url.split('/')[-1]}")

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx) -> tuple[Tensor, Tensor]:
        img_name = self.image_names[idx]
        image_tensor = self._load_or_download_image_tensor(img_name)
        labels_tensor = self._load_or_download_labels(img_name)
        return image_tensor, labels_tensor

    def _load_or_download_image_tensor(self, img_name: str) -> torch.Tensor:
        # tensor cache
        tensor_path = self.cache_root / self._subpath() / f"{img_name}.pth"
        if tensor_path.exists():
            return torch.load(tensor_path)

        # image .jpg cache
        img_path = self.saved_root / self._subpath() / img_name
        if not img_path.exists():
            self._download_file(img_name, img_path)

        # convert to tensor & cache
        image = Image.open(img_path).convert("RGB")
        image_tensor = self.transform(image)
        tensor_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(image_tensor, tensor_path)
        return image_tensor

    def _load_or_download_labels(self, img_name: str) -> torch.Tensor:
        label_name = img_name.replace(".jpg", ".txt").replace('.JPG', '.txt')
        label_path = self.cache_root / self._subpath("labels") / label_name
        if not label_path.exists():
            self._download_file(label_name, label_path, is_label=True)

        with open(label_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()

        # YOLO-format: class xc yc w h
        labels = []
        for line in lines:
            parts = list(map(float, line.strip().split()))
            labels.append(parts)

        return torch.tensor(labels, dtype=torch.float32)

    def _download_file(self, filename: str, save_path: Path, is_label=False):
        subfolder = f"{self.subfolder_path}/{'labels' if is_label else 'images'}"
        url = get_download_url(self.public_url, subfolder, filename)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        download_file_from_url(url, str(save_path))

    def _subpath(self, suffix="images") -> str:
        return f"{self.subfolder_path}/{suffix}".strip("/")
