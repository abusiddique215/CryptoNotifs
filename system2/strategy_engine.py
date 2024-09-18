from datetime import datetime, timedelta

class StrategyEngine:
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def time_based_strategy(self, coin_id, days, threshold, interval_hours=1):
        prices = self.historical_data.get_historical_prices(coin_id, days)
        if prices is None:
            return {}

        notifications = {}
        for timestamp, price in prices:
            dt = datetime.fromtimestamp(timestamp / 1000)
            hour = dt.replace(minute=0, second=0, microsecond=0)
            if price < threshold:
                if hour not in notifications:
                    notifications[hour] = 0
                notifications[hour] += 1

        return notifications

    def percentage_based_strategy(self, coin_id, days, percentage):
        prices = self.historical_data.get_historical_prices(coin_id, days)
        if prices is None:
            return []

        notifications = []
        peak = prices[0][1]
        for timestamp, price in prices:
            if price > peak:
                peak = price
            elif price < peak * (1 - percentage / 100):
                notifications.append((timestamp, price))
                peak = price  # Reset peak

        return notifications

    def custom_threshold_strategy(self, coin_id, days, initial_threshold, adjustment_factor):
        prices = self.historical_data.get_historical_prices(coin_id, days)
        if prices is None:
            return []

        notifications = []
        threshold = initial_threshold
        for timestamp, price in prices:
            if price < threshold:
                notifications.append((timestamp, price))
                threshold = price * (1 + adjustment_factor)  # Adjust threshold

        return notifications