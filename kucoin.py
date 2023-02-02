from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
from loguru import logger
from time import sleep

class KuCoin:
    def kucoin_listing(self, response):
        try:
            soup = self.make_soup(self.make_html(response))
            spans = soup.find_all('span')
            for span in spans:
                division = span.find_parents('div', {"class":"mainTitle___mbpq1"})
                if division != []:
                    start_date = span.parent.p.text
                    self.temp_listings.append(f"{span.text}\n{start_date}")

            if self.temp_listings == self.listings:
                pass
            else:
                self.listings_bot.send_message(self.t_id, {self.temp_listings[0]})
                logger.info(self.temp_listings[0])
            self.listings = self.temp_listings.copy()
            self.temp_listings.clear()
            logger.info('working')
        except Exception as e:
            logger.error(e)
            # logger.debug(response.html.raw_html)
            sleep(10)