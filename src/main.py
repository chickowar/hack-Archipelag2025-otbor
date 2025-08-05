from pathlib import Path

from pure_yolo.prepare import prepare_yolo_dataset
from pure_yolo.trainer import train_yolo


def main():
    # Путь до папки с изображениями
    image_dir = Path("src/yandex_image_getter/saved/wDp0Y3_KQ1Rlgw/Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue/images")
    assert image_dir.exists(), f"Папка не найдена: {image_dir}"

    # Собираем имена изображений
    image_names = sorted([p.name for p in image_dir.glob("*.jpg")])
    print(f"[Main] Найдено {len(image_names)} изображений")

    # URL и подкаталог на Яндекс.Диске
    public_url = "https://disk.yandex.ru/d/wDp0Y3_KQ1Rlgw"
    subfolder_path = "/Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue"

    # Подготовка датасета
    print("[Main] Подготовка YOLO-датасета...")
    prepare_yolo_dataset(public_url, subfolder_path, image_names)

    # Запуск обучения
    print("[Main] Запуск обучения YOLO-модели...")
    train_yolo()

    # Команда для TensorBoard
    print("\n[Main] ✅ Обучение завершено.")
    print("📊 Для просмотра логов запусти команду:")
    print("tensorboard --logdir runs/detect")


if __name__ == "__main__":
    main()
