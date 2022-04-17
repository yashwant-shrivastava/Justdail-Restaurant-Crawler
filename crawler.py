import re
from scrapper import Scrapper
import requests
from settings import get_random_user_agent


class PyCrawler(object):
    def __init__(self):
        self.starting_url = None
        self.visited = set()
        self.scrapper = Scrapper('testFile.csv')

    def get_html(self):
        try:
            useragents = get_random_user_agent()
            html = requests.get(
                self.starting_url,
                headers={
                    'USER-Agent': useragents,
                    'Host': 'www.justdial.com',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
            )
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self):
        html = self.get_html()
        links = re.findall('''<a\s+(?:[^>]*?\s+)href=[\']https\:\/\/www\.justdial\.com\/\S*-Restaurants\'>''', html)
        for i, link in enumerate(links):
            link = re.findall('''https://www.justdial.com/\S*-Restaurants''', link)[0]
            links[i] = link

        return set(filter(lambda x: 'mailto' not in x, links))

    def start(self, url):
        self.starting_url = url
        for link in self.get_links():
            print(link)
            if link in self.visited:
                continue
            self.visited.add(link)
            self.scrapper.start_scrapping(link)
