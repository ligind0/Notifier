from join import api_eth
from loguru import logger
from time import sleep

class Gas:

    def gas_price(self, response):
        try:
            response = eval(response.text)
            logger.info(response['result']['ProposeGasPrice'])
            # logger.info(type(response['result']['ProposeGasPrice']))
            if int(response['result']['ProposeGasPrice'])<14:
                alert = f"Alert gas {(response['result']['ProposeGasPrice'])}"
                logger.info(alert)
                self.gas_price_bot.send_message(self.t_id, alert)
                sleep(600)
            sleep(5)
        except Exception as e:
            logger.error(e)
            sleep(5)

def main():
    a = Gas()
    a.gas_price()

if __name__ == '__main__':
    main()