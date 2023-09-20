import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    titles = parser.findAll("tr", attrs={"class": "athing"})
    authors = parser.findAll("td", attrs={"class": "subtext"})
    for i in range(len(titles)):
        a = titles[i].findAll("td", attrs={"class": "title"})[1].find("a")
        title = a.get_text()
        url = a["href"]
        author = authors[i].find("a", attrs={"class": "hnuser"})
        if author:
            n_author = author.get_text()
        points = authors[i].find("span", attrs={"class": "score"})
        points = points.get_text()
        comments = authors[i].findAll("a")[-1].get_text()
        if "comments" in comments:
            comments = comments[0]
        else:
            comments = 0
        news_list.append(
            {
                "title": title,
                "author": n_author,
                "url": url,
                "comments": comments,
                "points": points,
            }
        )

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """
    Extract next page URL
    :param parser: BeautifulSoup web page object
    :return: next page URL or empty string if it isn't exist
    """
    next_page = parser.find("a", attrs={"class": "morelink"})
    if not next_page:
        return ""
    else:
        return next_page["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
