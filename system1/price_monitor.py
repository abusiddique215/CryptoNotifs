import asyncio
import logging
from system1.api_client import CoinGeckoAPI

class PriceMonitor:
    def __init__(self):
        self.api = CoinGeckoAPI()
        self.logger = logging.getLogger(__name__)
        self.tracked_coins = {}

    def add_coin(self, coin_id, threshold):
        self.tracked_coins[coin_id] = threshold
        self.logger.info(f"Added {coin_id} with threshold {threshold}")

    def remove_coin(self, coin_id):
        if coin_id in self.tracked_coins:
            del self.tracked_coins[coin_id]
            self.logger.info(f"Removed {coin_id} from tracking")

    async def check_price(self, coin_id, threshold):
        price = await self.api.get_current_price_async(coin_id)
        if price is not None:
            self.logger.info(f"Current price of {coin_id}: ${price}")
            if price < threshold:
                return coin_id, price
        return None

    async def check_prices(self):
        tasks = [self.check_price(coin_id, threshold) for coin_id, threshold in self.tracked_coins.items()]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def run(self, interval=10):
        while True:
            results = await self.check_prices()
            for coin_id, price in results:
                yield coin_id, price
            await asyncio.sleep(interval)