import string

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    #
    id = request.query.get("id")
    label = request.query.get("label")
    s = session()
    entry = s.query(News).get(id)
    #
    entry.label = label
    s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/update")
def update_news():
    news_s = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    news_bd = s.query(News).all()
    news_bd = [(n.title, n.author) for n in news_bd]
    for new in news_s:
        if (new["title"], new["author"]) not in news_bd:
            news = News(
                title=new["title"], author=new["author"], url=new["url"], comments=new["comments"], points=new["points"]
            )
            s.add(news)
            s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/classify")
def classify_news():  # type: ignore
    s = session()
    model = NaiveBayesClassifier(alpha=0.01)
    list_of_train = s.query(News).filter(News.label is not None).all()
    x_train = []
    y_train = []
    for i in list_of_train:
        x_train.append(i.title)
        y_train.append(i.label)
    model.fit(x_train, y_train)
    news = s.query(News).filter(News.label is None).all()
    x = [i.title for i in news]
    y = model.predict(x)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return sorted(news, key=lambda i: i.label)  # type: ignore


@route("/recommendations")
def recommendations():
        X, y, info = [], [], []
        s = session()
        for i in range(1001):
            for item in s.query(News).filter(News.id == i).all():
                X.append(item.title)
                y.append(item.label)
        X_test = []
        for i in range(1001, len(s.query(News).all()) + 1):
            for item in s.query(News).filter(News.id == i).all():
                X_test.append(item.title)
                info.append(News(author=item.author,
                                 points=item.points,
                                 comments=item.comments,
                                 url=item.url))
        X = [x.translate(str.maketrans("", "", string.punctuation)).lower() for x in X]
        X_cleared = [x.translate(str.maketrans("", "", string.punctuation)).lower() for x in X_test]
        model = NaiveBayesClassifier(alpha=0.01)
        model.fit(X, y)
        predicted_news = model.predict(X_cleared)
        classified_news = []
        for i in range(len(predicted_news) - 1):
            classified_news.append([y[i - 1], X_test[i - 1], info[i - 1]])
        classified_news = sorted(classified_news, key=lambda item: item[0])
        return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
