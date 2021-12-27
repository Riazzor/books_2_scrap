import os

from infrastructure.repository import save_book, save_image
from web_scraping.client import BASEURL, BookScraper

# Function doesn't support categorie update with new books
soup = BookScraper(BASEURL)
category_list = soup.get_all_category()


download_image = ''
while download_image not in ('Oui', 'Non'):
    download_image = input(
        'Télécharger les images de couvertures ? Si non, le programme sera plus rapide [oui/NON]\n'
    ).capitalize() or 'Non'

image_path = {
    'Oui': save_image,
    'Non': lambda image_url, image_name, category_name: False
}

# Before starting create Data/book/ and Data/image/
if not os.path.exists('./Data'):
    os.makedirs('./Data/book/')
    os.makedirs('./Data/image/')

if download_image == 'Oui':
    for category in category_list:
        os.makedirs('./Data/image/%s/' % category['name'])

for category in category_list:
    # import ipdb; ipdb.set_trace()
    category_books = soup.get_category_books(category['url'])
    for book in category_books:
        # If the user's' choice is yes, download image and put image_path in book['image_path']
        # else keep image url
        image = image_path.get(download_image)(
            book['image_url'],
            book['universal_product_code'],
            category['name']
        )
        if image:
            book['image_path'] = image
        save_book(book, category['name'])
