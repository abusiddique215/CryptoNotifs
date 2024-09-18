import aiohttp
import asyncio
import logging

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = None

    async def get_current_price_async(self, coin_id):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{self.BASE_URL}/simple/price?ids={coin_id}&vs_currencies=usd"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[coin_id]["usd"]
                else:
                    self.logger.error(f"Error fetching price for {coin_id}: HTTP {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Error fetching price for {coin_id}: {str(e)}")
            return None

    async def get_historical_prices_async(self, coin_id, days):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["prices"]
                else:
                    self.logger.error(f"Error fetching historical prices for {coin_id}: HTTP {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Error fetching historical prices for {coin_id}: {str(e)}")
            return None

    async def close(self):
        if self.session:
            await self.session.close()