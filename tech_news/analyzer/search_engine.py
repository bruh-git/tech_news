from datetime import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    news = search_news({"title": {"$regex": title, "$options": "i"}})
    return [(new["title"], new["url"]) for new in news]


# Requisito 7
def search_by_date(date):
    try:
        format_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        news = search_news({"timestamp": format_date})
        return [(new["title"], new["url"]) for new in news]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news_by_tags = search_news({"tags": {"$regex": tag, "$options": "i"}})
    return [(new["title"], new["url"]) for new in news_by_tags]


# Requisito 9
def search_by_category(category):
    news_by_category = search_news(
        {"category": {"$regex": category, "$options": "i"}}
    )
    return [(new["title"], new["url"]) for new in news_by_category]
