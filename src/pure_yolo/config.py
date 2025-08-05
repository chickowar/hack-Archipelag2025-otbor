from pathlib import Path

# 🗂️ Корневая директория проекта
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 📁 Директория с YOLO-датасетом
YOLO_DATASET_DIR = PROJECT_ROOT / "yolo_dataset"

# 📄 YAML-файл конфигурации для обучения
YOLO_DATA_YAML = PROJECT_ROOT / "yolo_dataset.yaml"

# 📦 Название модели YOLO (можно выбрать "yolov8n.pt", "yolov8s.pt", "yolov5s.pt" и т.п.)
YOLO_MODEL_NAME = "yolov8s.pt"

# ⚙️ Общие параметры обучения
TRAIN_PARAMS = {
    "epochs": 50,
    "imgsz": 640,
    "batch": 16,
    "device": "cuda",  # Обязательно использовать GPU
    "project": "runs/detect",
}
