import re

from requests import request
from bs4 import BeautifulSoup


BASEURL = "http://books.toscrape.com/"

# TODO : test with requests.get


def get_web_page(url: str) -> BeautifulSoup:
    web_page = request("get", url).text
    soup = BeautifulSoup(web_page, 'lxml')

    return soup


def get_book_cover(image_url):
    image = request('GET', image_url)
    content = False
    if image.ok:
        content = image.content
    return content


class CategoryBookScraper:
    def __init__(self, category_url) -> None:
        web_page = request('get', category_url).text
        self.url = category_url
        self.web_page = BeautifulSoup(web_page, 'lxml')

    def get_category_books(self, url: str) -> list:
        soup = self.get_web_page(url)

        book_list = soup.find_all(name='article', class_='product_pod')
        category_books = []
        for book in book_list:
            book_url = book.find('a')['href']
            # removing relative path and rebuilding absolute url
            book_url = '/'.join(
                elem for elem in book_url.split('/') if elem != '..'
            )

            book_url = BASEURL + 'catalogue/' + book_url
            book_info = self.get_book_info(book_url)
            category_books.append(book_info)

        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = next_page.find('a')['href']
            trunc_url = url[:url.rfind('/')] + '/'
            next_page_url = trunc_url + next_page_url
            for book in self.get_category_books(next_page_url):
                category_books.append(book)

        return category_books

    def get_book_info(self, book_url) -> dict:
        book_data = self.web_page.find(name='table').find_all('tr')

        # Number of book
        number_available = book_data[5].find('td').text
        number_available = re.search(
            r'(?P<nbr>\d+)',
            number_available
        ).group('nbr')

        # description
        previous_div = self.web_page.find(name='div', id='product_description')
        if previous_div:
            product_description = previous_div.find_next_sibling('p').text
        else:
            product_description = 'No description available ...'

        # rating
        rating = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5,
        }
        pararagraphe = self.web_page.find(name='p', class_='star-rating')
        classes = pararagraphe.get('class')
        review_rating = rating.get(classes[-1], 'Not available')

        # Both price with and without taxe
        price_including_tax = re.search(
            r'(?P<price>\d+.\d+)',
            book_data[3].find('td').text
        ).group('price')
        price_excluding_tax = re.search(
            r'(?P<price>\d+.\d+)',
            book_data[2].find('td').text
        ).group('price')

        # image url
        image_url = self.web_page.find('img').get('src')
        # removing relative path
        image_url = '/'.join(
            elem for elem in image_url.split('/') if elem != '..'
        )
        image_url = BASEURL + image_url

        # category
        breadcrumb_active = self.web_page.find(
            'ul', class_='breadcrumb').find('li', class_='active')
        category = breadcrumb_active.find_previous_sibling('li').text.strip()

        # Parsing data
        book_info = {
            "product_page_url": book_url,
            "universal_product_code": book_data[0].find('td').text,
            "title": self.web_page.h1.text,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "number_available": number_available,
            "product_description": product_description,
            "category": category,
            "review_rating": review_rating,
            "image_url": image_url,
        }

        return book_info


if __name__ == '__main__':
    book_scrapper = CategoryBookScraper(
        'http://books.toscrape.com/catalogue/the-requiem-red_995/index.html'
    )
    book_info = book_scrapper.get_book_info(
        'http://books.toscrape.com/catalogue/the-requiem-red_995/index.html'
    )
    print(book_info)
