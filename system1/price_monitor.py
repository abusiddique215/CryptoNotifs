import asyncio
from system1.api_client import CryptoAPI

class PriceMonitor:
    def __init__(self):
        self.api = CryptoAPI()
        self.tracked_coins = {}

    def add_coin(self, coin_id, threshold):
        self.tracked_coins[coin_id] = threshold
        asyncio.create_task(self.api.start_websocket([coin_id]))

    def remove_coin(self, coin_id):
        if coin_id in self.tracked_coins:
            del self.tracked_coins[coin_id]

    async def run(self, interval):
        while True:
            for coin_id, threshold in self.tracked_coins.items():
                price = await self.api.get_current_price(coin_id)
                if price is not None:
                    yield coin_id, price
            await asyncio.sleep(interval)

    def get_threshold(self, coin_id):
        return self.tracked_coins.get(coin_id)