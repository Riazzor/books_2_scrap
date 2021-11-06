"""
Iterating all book in a category page and saving them.
"""
from bs4 import BeautifulSoup

from client import get_web_page, BASEURL
from book_page import get_book_info


def get_category_books(url: str):
    category_page = get_web_page(url)

    doc = BeautifulSoup(category_page, 'lxml')
    book_list = doc.find_all(name='article', class_='product_pod')
    category_books = []
    for book in book_list:
        book_url = book.find('a')['href']
        # removing relative path and rebuilding absolute url
        book_url = '/'.join(
            elem for elem in book_url.split('/') if elem != '..'
        )
        book_url = BASEURL + 'catalogue/' + book_url
        book_info = get_book_info(book_url)
        category_books.append(book_info)

    return category_books
# TODO : recursive function for fetching next book if multiple page


if __name__ == '__main__':
    url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    print(*get_category_books(url), sep='\n\n')
