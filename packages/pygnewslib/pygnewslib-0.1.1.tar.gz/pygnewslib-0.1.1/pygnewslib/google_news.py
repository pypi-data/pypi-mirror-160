import feedparser
from bs4 import BeautifulSoup as Soup

from pygnewslib.constants import countries, languages


class GoogleNews:

    def __init__(self, lang="en", country="US", max_results=10):
        self.countries = tuple(countries),
        self.languages = tuple(languages),
        self._max_results = max_results
        self.lang = lang
        self.country = country
        self.BASE_URL = 'https://news.google.com/rss'

    def ceid(self):
        return '&ceid={}:{}&hl={}&gl={}'.format(self.country,
                                                self.lang,
                                                self.lang,
                                                self.country)

    @property
    def language(self):
        return self.lang

    @language.setter
    def language(self, language):
        self.lang = languages.get(language, language)

    @property
    def max_results(self):
        return self._max_results

    @max_results.setter
    def max_results(self, size):
        self._max_results = size

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = countries.get(country, country)

    def clean(self, html):
        soup = Soup(html, features="html.parser")
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def news_data(self, item):
        item = {
            'title': item.get("title", ""),
            'description': self.clean(item.get("description", "")),
            'published date': item.get("published", ""),
            'url': item.get("link", ""),
            'publisher': item.get("source", " ")
        }
        return item

    def fetch_news(self, key):
        if key != '':
            key = "%20".join(key.split(" "))
            url = self.BASE_URL + '/search?q={}'.format(key) + self.ceid()
            return list(map(self.news_data, feedparser.parse(url).entries[:self._max_results]))
