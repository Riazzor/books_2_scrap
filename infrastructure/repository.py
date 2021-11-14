import csv
import os
import re

from web_scraping.book_page import get_book_info
from web_scraping.client import get_book_cover


def save_image(image_url: str, image_name: str, category_name: str):
    """
    Function save image in Data_image and return path to image
    """
    # on first book of category, create Data/image/category
    category_name = category_name.replace(' ', '_')
    if not os.path.exists(f"./Data/image/{category_name}/"):
        os.makedirs(f"./Data/image/{category_name}/")

    content = get_book_cover(image_url)
    # replace none alphanumerical character with '_'
    image_name = re.sub(r'[^\w]+', '_', image_name)
    image_path = f'Data/image/{category_name}/{image_name}.jpg'
    with open(image_path, 'wb') as image_file:
        image_file.write(content)

    return image_path


def save_book(book_info: dict, category: str = 'uncategorized') -> None:
    """One csv file per category with each book in it."""

    csv_columns = book_info.keys()
    csv_file = f"Data/book/{category}.csv"

    # If file doesn't exist, we need to write the header first :
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=csv_columns
            )
            writer.writeheader()

    with open(csv_file, 'a') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=csv_columns
        )
        writer.writerow(book_info)


if __name__ == "__main__":
    book_info = get_book_info(
        'http://books.toscrape.com/catalogue/the-requiem-red_995/index.html'
    )
    save_book(book_info)
    image_url = book_info['image_url']
    image_name = book_info['title']
    category = book_info['category']
    save_image(image_url, image_name, category)
