from yandex_image_getter.download import download_images_by_names, ensure_names_cache

if __name__ == '__main__':
    public_url = "https://disk.yandex.ru/d/wDp0Y3_KQ1Rlgw"

    output_dir = 'src/yandex_image_getter/saved/wDp0Y3_KQ1Rlgw/' \
    'Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue' \
    '/images'

    print(f'Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue/images')
    subfolder_path = f'/Вариант скачивания №1 — Отдельные снимки/02_part_dataset_human_rescue/images'
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