from requests import request
from bs4 import BeautifulSoup


BASEURL = "http://books.toscrape.com/"


def get_web_page(url: str) -> BeautifulSoup:
    web_page = request("get", url).text
    soup = BeautifulSoup(web_page, 'lxml')

    return soup
