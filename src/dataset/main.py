import os

from dataset.YaDiskDataset import YaDiskDataset
from dataset.display import show_sample
from yandex_image_getter.download import download_n_random_images

if __name__ == '__main__':
    public_url = "https://disk.yandex.ru/d/wDp0Y3_KQ1Rlgw"
    subfolder_path = '/Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue'
    output_path = f"src/yandex_image_getter/saved/{public_url.split('/')[-1]}{subfolder_path}/images"
    download_n_random_images(public_url, subfolder_path + '/images', output_path, 1000)
    names_list = os.listdir(output_path)
    ds = YaDiskDataset(public_url, subfolder_path, names_list)
    print(ds[0][0].shape)
    print(len(ds))
    show_sample(ds[0])
