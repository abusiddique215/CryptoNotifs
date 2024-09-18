import aiohttp
import asyncio
import logging
import json
from websockets import connect

class CryptoAPI:
    COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
    BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.websocket = None
        self.prices = {}

    async def get_current_price(self, coin_id):
        # First, check if we have a real-time price from WebSocket
        if coin_id in self.prices:
            return self.prices[coin_id]

        # If not, fall back to CoinGecko API
        url = f"{self.COINGECKO_BASE_URL}/simple/price?ids={coin_id}&vs_currencies=usd"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[coin_id]["usd"]
                    else:
                        self.logger.error(f"Error fetching price for {coin_id}: HTTP {response.status}")
                        return None
        except Exception as e:
            self.logger.error(f"Error fetching price for {coin_id}: {str(e)}")
            return None

    async def get_historical_prices(self, coin_id, days):
        url = f"{self.COINGECKO_BASE_URL}/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["prices"]
                    else:
                        self.logger.error(f"Error fetching historical prices for {coin_id}: HTTP {response.status}")
                        return None
        except Exception as e:
            self.logger.error(f"Error fetching historical prices for {coin_id}: {str(e)}")
            return None

    async def start_websocket(self, symbols):
        self.websocket = await connect(self.BINANCE_WS_URL)
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}usdt@trade" for symbol in symbols],
            "id": 1
        }
        await self.websocket.send(json.dumps(subscribe_message))
        asyncio.create_task(self._handle_websocket_messages())

    async def _handle_websocket_messages(self):
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                if 'e' in data and data['e'] == 'trade':
                    symbol = data['s'][:-4].lower()  # Remove 'USDT' and convert to lowercase
                    price = float(data['p'])
                    self.prices[symbol] = price
            except Exception as e:
                self.logger.error(f"WebSocket error: {str(e)}")
                await asyncio.sleep(5)  # Wait before attempting to reconnect

    async def stop_websocket(self):
        if self.websocket:
            await self.websocket.close()