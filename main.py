from crawler import PyCrawler
import requests


if __name__ == '__main__':
    crawler = PyCrawler()
    crawler.start("https://www.justdial.com/Jabalpur/Restaurant-Collections/AllCategory")

    #
    # page_number = 1
    # while True:
    #     html = requests.get(
    #         "https://www.justdial.com/Jabalpur/Italian-Restaurants/nct-10278125/page-{}".format(page_number),
    #         headers={
    #             'USER-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
    #             'Host': 'www.justdial.com',
    #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #             'Accept-Language': 'en-US,en;q=0.5',
    #             'Accept-Encoding': 'gzip, deflate, br',
    #             'Connection': 'keep-alive'
    #         }
    #     )
    #
    #     print(html.url)
    #     for res in html.history:
    #         print(res.url)
    #
    #     page_number += 1