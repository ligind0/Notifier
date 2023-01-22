from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
from loguru import logger

class Binance:
    def binance_listing(self, soup_binance):
        try:
            binance_list = soup_binance.find_all('div', {"class": "css-k5e9j4"})
            firstlink = binance_list[0].a['href']
            urls = []
            urls.append(f"{self.url_binance}{firstlink}")
            all_responses = self.asession.run(*[lambda url=url: self.get_url(url) for url in urls])
            for response in all_responses:
                soup_test = self.make_soup(response)
                info_list = soup_test.find_all('strong', {"class": "css-1lohbqv"})
                info = info_list[1].parent.text
                logger.debug("It's fine I'm working")
                if self.temp_binance != info:
                    logger.info(f'Sending message to binance listings like this:')
                    logger.info(f'{info}')
                    logger.info(f'{firstlink}')
                    self.binance_news.send_message(self.t_id, f'{info}\n{f"{self.url_binance}{firstlink}"}')
                self.temp_binance = info
        except Exception as e:
            logger.error(e)