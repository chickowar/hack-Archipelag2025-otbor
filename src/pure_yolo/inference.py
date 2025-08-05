from ultralytics import YOLO
from pathlib import Path
import cv2
from pure_yolo.config import YOLO_DATASET_DIR


def run_inference(
    model_path: str,
    image_dir: Path = YOLO_DATASET_DIR / "images/val",
    save: bool = True,
    show: bool = False,
    save_dir: Path = Path("predictions")
):
    """
    Применяет обученную YOLO модель к изображениям.
    :param model_path: Путь к .pt файлу (обычно best.pt)
    :param image_dir: Папка с изображениями
    :param save: Сохранять ли результат
    :param show: Показывать ли окно с результатами
    :param save_dir: Куда сохранять предсказания
    """
    model = YOLO(model_path)
    image_paths = list(image_dir.glob("*.jpg"))
    if not image_paths:
        print(f"[Inference] ❌ Нет изображений в {image_dir}")
        return

    if save:
        save_dir.mkdir(parents=True, exist_ok=True)

    for img_path in image_paths:
        results = model(img_path)

        # Отрисовка
        for r in results:
            im_array = r.plot()  # numpy array with bboxes
            if save:
                out_path = save_dir / img_path.name
                cv2.imwrite(str(out_path), im_array)
            if show:
                cv2.imshow("YOLO Detection", im_array)
                key = cv2.waitKey(0)
                if key == 27:  # Esc
                    break
    if show:
        cv2.destroyAllWindows()

    print(f"[Inference] ✅ Обработка завершена. Сохранено в: {save_dir.resolve()}")
