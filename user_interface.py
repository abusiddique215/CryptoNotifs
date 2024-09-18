import asyncio
from system1.price_monitor import PriceMonitor
from system2.log_manager import LogManager
from system2.notification_manager import NotificationManager
from system2.strategy_engine import StrategyEngine
from system1.historical_data import HistoricalData

class UserInterface:
    def __init__(self, price_monitor, log_manager, notification_manager, strategy_engine, historical_data):
        self.price_monitor = price_monitor
        self.log_manager = log_manager
        self.notification_manager = notification_manager
        self.strategy_engine = strategy_engine
        self.historical_data = historical_data

    async def main_menu(self):
        while True:
            print("\nCryptocurrency Price Tracker")
            print("1. Add coin to track")
            print("2. Remove coin from tracking")
            print("3. View tracked coins")
            print("4. View logs")
            print("5. Run simulation")
            print("6. Analyze logs")
            print("7. Re-feed logs")
            print("8. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                await self.add_coin()
            elif choice == '2':
                await self.remove_coin()
            elif choice == '3':
                self.view_tracked_coins()
            elif choice == '4':
                self.view_logs()
            elif choice == '5':
                await self.run_simulation()
            elif choice == '6':
                self.analyze_logs()
            elif choice == '7':
                self.re_feed_logs()
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")

    async def add_coin(self):
        coin_id = input("Enter the coin ID (e.g., bitcoin): ")
        threshold = float(input("Enter the price threshold: "))
        email = input("Enter your email for notifications: ")
        self.price_monitor.add_coin(coin_id, threshold)
        self.notification_manager.add_notification(coin_id, email)
        print(f"Added {coin_id} with threshold ${threshold}")

    async def remove_coin(self):
        coin_id = input("Enter the coin ID to remove: ")
        self.price_monitor.remove_coin(coin_id)
        self.notification_manager.remove_notification(coin_id)
        print(f"Removed {coin_id} from tracking")

    def view_tracked_coins(self):
        print("\nCurrently tracked coins:")
        for coin_id, threshold in self.price_monitor.tracked_coins.items():
            print(f"{coin_id}: threshold ${threshold}")

    def view_logs(self):
        print("\nRecent logs:")
        logs = self.log_manager.get_recent_logs(10)  # Get last 10 logs
        for log in logs:
            print(log)

    async def run_simulation(self):
        coin_id = input("Enter the coin ID for simulation: ")
        days = int(input("Enter the number of days for historical data: "))
        threshold = float(input("Enter the price threshold for simulation: "))
        
        print(f"Running simulation for {coin_id} over {days} days with threshold ${threshold}")
        
        historical_prices = await self.historical_data.get_historical_prices_async(coin_id, days)
        if historical_prices is None:
            print("Failed to fetch historical data.")
            return

        print("\nTime-based strategy:")
        time_based = await self.strategy_engine.time_based_strategy(coin_id, days, threshold)
        print(f"Notifications: {len(time_based)}")

        print("\nPercentage-based strategy:")
        percentage = float(input("Enter the percentage for price drop (e.g., 5 for 5%): "))
        percentage_based = await self.strategy_engine.percentage_based_strategy(coin_id, days, percentage)
        print(f"Notifications: {len(percentage_based)}")

        print("\nCustom threshold strategy:")
        adjustment_factor = float(input("Enter the adjustment factor (e.g., 0.05 for 5%): "))
        custom_threshold = await self.strategy_engine.custom_threshold_strategy(coin_id, days, threshold, adjustment_factor)
        print(f"Notifications: {len(custom_threshold)}")

        self.log_manager.log_strategy_simulation("time_based", coin_id, {"days": days, "threshold": threshold}, len(time_based))
        self.log_manager.log_strategy_simulation("percentage_based", coin_id, {"days": days, "percentage": percentage}, len(percentage_based))
        self.log_manager.log_strategy_simulation("custom_threshold", coin_id, {"days": days, "initial_threshold": threshold, "adjustment_factor": adjustment_factor}, len(custom_threshold))

    def analyze_logs(self):
        self.log_manager.analyze_logs()

    def re_feed_logs(self):
        self.log_manager.re_feed_logs(self.price_monitor, self.notification_manager)