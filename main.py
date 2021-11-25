import os

from infrastructure.repository import save_book, save_image
from web_scraping.client import BASEURL, get_web_page
from web_scraping.category_page import get_category_books

# Function doesn't support categorie update with new books
soup = get_web_page(BASEURL)
category_list = soup.find('ul', class_='nav-list').find('ul').find_all('li')


download_image = ''
while download_image not in ('Oui', 'Non'):
    download_image = 'Non'
    download_image = input(
        'Télécharger les images de couvertures ? Si non, le programme sera plus rapide [oui/NON]\n'
    ).capitalize() or download_image

image_path = {
    'Oui': save_image,
    'Non': lambda image_url, image_name, category_name: False
}

# Before starting create Data/book/ and Data/image/
if not os.path.exists('./Data'):
    os.makedirs('./Data/book/')
    os.makedirs('./Data/image/')

for category in category_list:
    link = category.find('a')
    cat_url = BASEURL + link['href']
    category_name = link.text.strip().replace(' ', '_')
    category_books = get_category_books(cat_url)
    if download_image == 'Oui':
        os.makedirs(f'./Data/image/{category_name}/')
    for book in category_books:
        # If the user's' choice is yes, download image and put image_path in book['image_path']
        # else keep image url
        image = image_path.get(download_image)(
            book['image_url'],
            book['universal_product_code'],
            category_name
        )
        if image:
            book['image_path'] = image
        save_book(book, category_name)
