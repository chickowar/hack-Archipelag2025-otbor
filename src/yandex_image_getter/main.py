from yandex_image_getter.download import download_images_by_names, ensure_names_cache

if __name__ == '__main__':
    public_url = "https://disk.yandex.ru/d/wDp0Y3_KQ1Rlgw"

    output_dir = 'src/yandex_image_getter/saved/wDp0Y3_KQ1Rlgw/' \
    'Вариант скачивания №1 — Отдельные снимки/03_part_dataset_human_rescue' \
    '/03_part_dataset_human_rescue1/images'

    for i in list(map(lambda x: f"{x:02}", range(1, 16))) + ['19', '35']:
        print(f'Вариант скачивания №1 — Отдельные снимки/01_part_dataset_human_rescue/images/{i}')
        subfolder_path = f'/Вариант скачивания №1 — Отдельные снимки/01_part_dataset_human_rescue/images/{i}'
        names = ensure_names_cache(
            public_url=public_url,
            subfolder_path=subfolder_path
        )
        print(len(names))
        download_images_by_names(
            public_url,
            subfolder_path,
            output_dir,
            names
        )