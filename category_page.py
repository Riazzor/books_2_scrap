"""
Iterating all book in a category page and saving them.
"""

from client import get_web_page, BASEURL
from book_page import get_book_info

# @pagination


def get_category_books(url: str):
    soup = get_web_page(url)

    book_list = soup.find_all(name='article', class_='product_pod')
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

    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = next_page.find('a')['href']
        trunc_url = url[:url.rfind('/')] + '/'
        next_page_url = trunc_url + next_page_url
        for book in get_category_books(next_page_url):
            category_books.append(book)

    return category_books


if __name__ == '__main__':
    url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    print(len(get_category_books(url)))
