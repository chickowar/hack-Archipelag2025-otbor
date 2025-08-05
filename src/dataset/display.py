import matplotlib.pyplot as plt
import matplotlib.patches as patches
import torch

def show_sample(sample, figsize=(8, 8), class_names=None):
    """
    sample: tuple (image_tensor, label_tensor), как возвращает dataset[i]
    class_names: список имён классов (если нужно отобразить подписи)
    """
    image_tensor, label_tensor = sample

    if not isinstance(image_tensor, torch.Tensor):
        raise ValueError("Первый элемент должен быть torch.Tensor")

    # Перевод из [C, H, W] -> [H, W, C] и в numpy
    image_np = image_tensor.permute(1, 2, 0).numpy()

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.imshow(image_np)

    h, w = image_tensor.shape[1:]

    for label in label_tensor:
        cls, xc, yc, bw, bh = label.tolist()

        # YOLO формат: центр и размер -> левый верхний угол
        x0 = (xc - bw / 2) * w
        y0 = (yc - bh / 2) * h
        box_w = bw * w
        box_h = bh * h

        rect = patches.Rectangle(
            (x0, y0),
            box_w,
            box_h,
            linewidth=2,
            edgecolor='lime',
            facecolor='none'
        )
        ax.add_patch(rect)

        if class_names:
            ax.text(x0, y0 - 2, class_names[int(cls)],
                    fontsize=10, color='white', backgroundcolor='black')

    ax.axis('off')
    plt.tight_layout()
    plt.show()
