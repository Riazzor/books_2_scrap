import os

from infrastructure.repository import save_book, save_image
from web_scraping.client import BASEURL, get_web_page
from web_scraping.category_page import get_category_books

# Function doesn't support categorie update with new books
soup = get_web_page(BASEURL)
category_list = soup.find('ul', class_='nav-list').find('ul').find_all('li')
download_image = ''
while download_image not in ('Yes', 'No'):
    download_image = 'No'
    download_image = input(
        'Télécharger les images de couvertures ?[yes/No]\n'
    ).capitalize() or download_image

image_path = {
    'Yes': save_image,
    'No': lambda image_url, image_name, category_name: False
}

# On first book create Data/book/
if not os.path.exists("./Data/book/"):
    os.makedirs("./Data/book/")

for category in category_list:
    link = category.find('a')
    cat_url = BASEURL + link['href']
    category_name = link.text.strip()
    category_books = get_category_books(cat_url)
    for book in category_books:
        # If the user's' choice is yes, download image and put image_path in book['image_url']
        # else keep image url
        image = image_path.get(download_image)(
            book['image_url'],
            book['title'],
            category_name
        )
        book['image_url'] = image or book['image_url']
        save_book(book, category_name)
