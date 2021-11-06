from requests import request


BASEURL = "http://books.toscrape.com/"


def get_web_page(url):
    return request("get", url).text
