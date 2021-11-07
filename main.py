from infrastructure.repository import save_book
from web_scraping.client import BASEURL, get_web_page
from web_scraping.category_page import get_category_books

soup = get_web_page(BASEURL)
category_list = soup.find('ul', class_='nav-list').find('ul').find_all('li')
# print(category_list)


for category in category_list:
    link = category.find('a')
    cat_url = BASEURL + link['href']
    cat_name = link.text.strip()
    category_books = get_category_books(cat_url)
    for book in category_books:
        save_book(book, cat_name)
