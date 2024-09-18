from system1.api_client import CoinGeckoAPI

class HistoricalData:
    def __init__(self):
        self.api = CoinGeckoAPI()

    def get_historical_prices(self, coin_id, days):
        return self.api.get_historical_prices(coin_id, days)

    def simulate_notifications(self, coin_id, days, threshold):
        prices = self.get_historical_prices(coin_id, days)
        if prices is None:
            return []

        notifications = []
        for timestamp, price in prices:
            if price < threshold:
                notifications.append((timestamp, price))

        return notifications