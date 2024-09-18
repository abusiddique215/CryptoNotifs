from system1.api_client import CryptoAPI

class HistoricalData:
    def __init__(self):
        self.api = CryptoAPI()

    async def get_historical_prices(self, coin_id, days):
        # This method needs to be implemented in the CryptoAPI class
        return await self.api.get_historical_prices(coin_id, days)

    async def simulate_notifications(self, coin_id, days, threshold):
        prices = await self.get_historical_prices(coin_id, days)
        if prices is None:
            return []

        notifications = []
        for timestamp, price in prices:
            if price < threshold:
                notifications.append((timestamp, price))

        return notifications