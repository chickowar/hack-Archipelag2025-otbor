from ultralytics import YOLO
from .config import YOLO_DATA_YAML, YOLO_MODEL_NAME, TRAIN_PARAMS
from datetime import datetime


def train_yolo(name: str = None):
    """
    Обучает YOLO модель с использованием Ultralytics API.
    :param name: Название эксперимента (по умолчанию auto)
    """
    name = name or datetime.now().strftime("exp_%Y%m%d_%H%M%S")
    print(f"[Trainer] Запуск обучения модели {YOLO_MODEL_NAME}...")

    # Загружаем предобученную модель
    model = YOLO(YOLO_MODEL_NAME)

    # Запуск обучения
    model.train(
        data=str(YOLO_DATA_YAML),
        epochs=TRAIN_PARAMS["epochs"],
        imgsz=TRAIN_PARAMS["imgsz"],
        batch=TRAIN_PARAMS["batch"],
        device=TRAIN_PARAMS["device"],
        project=TRAIN_PARAMS["project"],
        name=name,
        save=True,
        verbose=True,
    )

    print(f"[Trainer] ✅ Обучение завершено. Модель сохранена в: {TRAIN_PARAMS['project']}/{name}")
    print(f"[Trainer] 📊 Запусти `tensorboard --logdir {TRAIN_PARAMS['project']}` чтобы отслеживать метрики")
