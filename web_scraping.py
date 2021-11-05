import re

from bs4 import BeautifulSoup
import requests

BASEURL = "http://books.toscrape.com/"


def get_book_info(url: str) -> dict:
    book_page = requests.get(url).text

    doc = BeautifulSoup(book_page, 'lxml')
    book_data = doc.find(name='table').find_all('tr')

    # TODO : image_url
    # TODO : price regex

    number_available = book_data[5].find('td').text
    number_available = re.search(
        r'(?P<nbr>\d+)', number_available
    ).group('nbr')

    previous_div = doc.find(name='div', id='product_description')
    product_description = previous_div.find_next_sibling('p').text

    par = doc.find(name='p', class_='star-rating')
    classes = par.get('class')
    review_rating = classes[-1]
    
    book_info = {
        "product_page_url": url,
        "universal_product_code": book_data[0].find('td').text,
        "title": doc.h1.text,
        "price_including_tax": book_data[3].find('td').text,
        "price_excluding_tax": book_data[2].find('td').text,
        "number_available": number_available,
        "product_description": product_description,
        "category": book_data[1].find('td').text,
        "review_rating": review_rating,
    }

    print(par.get('class')[-1])
    return book_info


if __name__ == "__main__":
    url = BASEURL + "catalogue/old-records-never-die-one-mans-quest-for-his-vinyl-and-his-past_39/index.html"
    book_info = get_book_info(url)
    print(*[f"{k}: {v}" for k, v in book_info.items()], sep="\n")


# TODO : AREPL VS Jupyter
