import requests
import unicodedata
from bs4 import BeautifulSoup

URL_start = "https://lenta.ru/"
url_body = ""
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
           'accept': '*/*'}


def get_connect(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_news_title(html):
    global URL_start
    global url_body
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("div", class_="first-item")
    date = item.find("time").get("datetime")
    pict = item.find("img").get("src")
    title = item.find_all("a")[1].text[5:]
    title = unicodedata.normalize("NFKD", title)
    url_body = URL_start + item.find_all("a")[1].get("href")
    news = {'date': date,
            'pict': pict,
            'title': title}
    return news


def get_news_body(html):
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find("p")
    return item.text


def parse(body=False):
    html = get_connect(URL_start)
    if html.status_code == 200:
        news = get_news_title(html.text)
    else:
        return "error 404"
    if body:
        html = get_connect(url_body)
        if html.status_code == 200:
            return get_news_body(html.text)
    return news


if __name__ == "__main__":
    parse(body=True)