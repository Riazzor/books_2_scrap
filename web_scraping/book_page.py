"""
Parsing all book info in page and
returning them as a dict.
"""

import re

from web_scraping.client import get_web_page, BASEURL


def get_book_info(url: str) -> dict:
    soup = get_web_page(url)

    book_data = soup.find(name='table').find_all('tr')

    number_available = book_data[5].find('td').text
    number_available = re.search(
        r'(?P<nbr>\d+)',
        number_available
    ).group('nbr')

    previous_div = soup.find(name='div', id='product_description')
    if previous_div:
        product_description = previous_div.find_next_sibling('p').text
    else:
        product_description = 'No description available ...'

    par = soup.find(name='p', class_='star-rating')
    classes = par.get('class')
    review_rating = classes[-1]

    price_including_tax = re.search(
        r'(?P<price>\d+.\d+)',
        book_data[3].find('td').text
    ).group('price')
    price_excluding_tax = re.search(
        r'(?P<price>\d+.\d+)',
        book_data[2].find('td').text
    ).group('price')

    image_url = soup.find('img').get('src')
    # removing relative path
    image_url = '/'.join(
        elem for elem in image_url.split('/') if elem != '..'
    )
    image_url = BASEURL + image_url

    book_info = {
        "product_page_url": url,
        "universal_product_code": book_data[0].find('td').text,
        "title": soup.h1.text,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": book_data[1].find('td').text,
        "review_rating": review_rating,
        "image_url": image_url,
    }

    return book_info


if __name__ == "__main__":
    url = BASEURL + "catalogue/old-records-never-die-one-mans-quest-for-his-vinyl-and-his-past_39/index.html"
    book_info = get_book_info(url)
    print(*[f"{k}: {v}" for k, v in book_info.items()], sep="\n")
