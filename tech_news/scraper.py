import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url: str, wait: int = 1) -> str:
    try:
        response = requests.get(url, timeout=3, headers={
            "user-agent": "Fake user-agent"
        })
        time.sleep(wait)
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content) -> list:
    selector = Selector(html_content)
    url = "article.entry-preview h2.entry-title a::attr(href)"
    return selector.css(url).getall()


# Requisito 3
def scrape_next_page_link(html_content) -> list:
    selector = Selector(html_content)
    url = "a.next.page-numbers::attr(href)"
    return selector.css(url).get()


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
