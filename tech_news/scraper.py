import requests
import time
from parsel import Selector
from tech_news.database import create_news


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
    selector = Selector(html_content)
    news = {
        "url": selector.css("link[rel='canonical']::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span.author a::text").get(),
        "comments_count": len(selector.css("comment-list").getall()),
        "summary": "".join(
            selector.css(
                "div.entry-content > p:nth-of-type(1) ::text"
            ).getall()
        ).strip(),
        "tags": selector.css(
            "section.post-tags li a[rel='tag']::text"
        ).getall(),
        "category": selector.css("span.label::text").get(),
    }

    return news


# Requisito 5
def get_tech_news(amount):
    news = []
    url = "https://blog.betrybe.com/"

    while len(news) < amount:
        html_content = fetch(url)
        links = scrape_novidades(html_content)

        for link in links:
            if len(news) < amount:
                html = fetch(link)
                link = scrape_noticia(html)
                news.append(link)
            else:
                break
        url = scrape_next_page_link(html_content)
    create_news(news)
    return news
