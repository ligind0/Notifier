from requests_html import AsyncHTMLSession, HTMLSession, HTMLResponse
from bs4 import BeautifulSoup
import telebot
from loguru import logger
from time import sleep
from threading import Thread
from join import token_binance, token_listings, token_gas_price, t_id, api_eth, proxy
from gas_price import Gas
from binance import Binance
from kucoin import KuCoin

class Notifier(Gas, Binance, KuCoin):

    def __init__(self, autostart=True):
        self.asession = AsyncHTMLSession()
        self.url_binance = 'https://www.binance.com'
        #KuCoin
        self.temp_listings = []
        self.temp_binance = None
        self.listings = []
        self.proxies = proxy
        self.listings_bot = telebot.TeleBot(token_listings)
        self.gas_price_bot = telebot.TeleBot(token_gas_price)
        self.binance_news = telebot.TeleBot(token_binance)
        # self.gas_price_bot.config['api_key'] = token_gas_price
        # self.listings_bot.config['api_key'] = token_listings
        # self.binance_news.config['api_key'] = token_binance
        # Private Area
        self.t_id = t_id
        self.processes = [self.gas_price]
        self.parsing_processes = [self.kucoin_listing, self.binance_listing, self.gas_price]
        self.parsing_urls = ['https://www.kucoin.com/news/categories/listing', f'{self.url_binance}/en/support/announcement/new-cryptocurrency-listing?c=48', f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_eth}'] #

        if autostart:
            self.run()

    async def get_url(self, url):
        try:
            logger.debug(f'getting {url}')
            r = await self.asession.get(url, proxies=self.proxies)
            await r.html.arender(timeout=70)
            return {'url': url, 'response': r}
        except Exception as e:
            logger.error(e)

    def make_soup(self, html):
        if isinstance(html, (str, bytes)):    
            soup = BeautifulSoup(html, features='html.parser')
            return soup
        else:
            raise ValueError("Variable html must be str or bytes type")


    def make_html(self, response):
        if isinstance(response, HTMLResponse):
            return response.html.raw_html
        elif isinstance(response, requests.models.Response):
            return response.text
        else:
            raise ValueError(f"Got wrong type of value {response}")

    def parsing(self):

        while True:
            try:
                results = self.asession.run(*[lambda url=url: self.get_url(url) for url in self.parsing_urls])
                print(results)
                for i, url in enumerate(self.parsing_urls):
                    logger.debug(url)
                    for result in results:

                        if result['url'] == url:
                            logger.debug(f"result {result['url']} is {url} calling {self.parsing_processes[i].__name__}")
                            self.parsing_processes[i](result['response'])

                sleep(35)
            except Exception as e:
                logger.error(e)
                sleep(35)


    def run(self):
        self.parsing()
        



def main():
    a = Notifier(True)


if __name__ == '__main__':
    main()


