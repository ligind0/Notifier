import requests
import urllib.request
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import telebot
from loguru import logger
from time import sleep
from threading import Thread
from join import token_binance, token_listings, token_gas_price, t_id, api_eth
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
        self.proxies = {
       'http': 'http://5.189.157.63:8080'
       # 'https': 'http://5.189.157.63:8080',
        }
        self.listings_bot = telebot.TeleBot(token_listings)
        self.gas_price_bot = telebot.TeleBot(token_gas_price)
        self.binance_news = telebot.TeleBot(token_binance)
        # self.gas_price_bot.config['api_key'] = token_gas_price
        # self.listings_bot.config['api_key'] = token_listings
        # self.binance_news.config['api_key'] = token_binance
        # Private Area
        self.t_id = t_id
        self.processes = [self.gas_price]

        if autostart:
            self.run()

    async def get_url(self, url):
        try:
           r = await self.asession.get(url, proxies=self.proxies)
           await r.html.arender(timeout=50)
           return r
        except Exception as e:
           logger.error(e)

    def make_soup(self, response):
        logger.debug(response)
        soup = BeautifulSoup(response.html.raw_html, features='html.parser')
        return soup

    def run(self):
        for process in self.processes:
            logger.info(process.__name__)
            th = Thread(target=self.infiniteloopfunc, args=[process])
            th.start()
        while True:
            sleep(60)
            urls = ['https://www.kucoin.com/news/categories/listing', f'{self.url_binance}/en/support/announcement/new-cryptocurrency-listing?c=48']
            result = self.asession.run(*[lambda url=url: self.get_url(url) for url in urls])
            soup_binance = self.make_soup(result[1])
            soup_kucoin = self.make_soup(result[0])
            
            self.kucoin_listing(soup_kucoin)
            self.binance_listing(soup_binance)

    def infiniteloopfunc(self, process):
        while True:
            process()          

def main():
    Notifier()


if __name__ == '__main__':
    main()



