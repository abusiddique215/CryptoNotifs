import asyncio
import logging
from system1.price_monitor import PriceMonitor
from system1.historical_data import HistoricalData
from system2.notification_manager import NotificationManager
from system2.log_manager import LogManager
from system2.strategy_engine import StrategyEngine
from config import EMAIL_CONFIG, CHECK_INTERVAL, LOG_FILE, LOG_LEVEL

logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CryptoTracker:
    def __init__(self):
        self.price_monitor = PriceMonitor()
        self.notification_manager = NotificationManager(EMAIL_CONFIG)
        self.log_manager = LogManager(LOG_FILE)
        self.historical_data = HistoricalData()
        self.strategy_engine = StrategyEngine(self.historical_data)

    async def start(self):
        # Initialize WebSocket connections for all tracked coins
        for coin_id in self.price_monitor.tracked_coins:
            await self.price_monitor.api.start_websocket([coin_id])

    async def monitor_prices(self):
        async for coin_id, price in self.price_monitor.run(interval=CHECK_INTERVAL):
            threshold = self.price_monitor.get_threshold(coin_id)
            if price < threshold:
                self.notification_manager.notify(coin_id, price, threshold)

    async def add_coin(self):
        coin_id = input("Enter the coin ID (e.g., bitcoin): ")
        threshold = float(input("Enter the price threshold: "))
        email = input("Enter your email for notifications: ")
        self.price_monitor.add_coin(coin_id, threshold)
        self.notification_manager.add_notification(coin_id, email)
        self.log_manager.log_info(f"Added {coin_id} with threshold ${threshold:.2f} for notifications to {email}")
        print(f"Added {coin_id} with threshold ${threshold:.2f} for notifications to {email}")

    async def remove_coin(self):
        coin_id = input("Enter the coin ID to remove: ")
        self.price_monitor.remove_coin(coin_id)
        self.log_manager.log_info(f"Removed {coin_id} from tracking")
        print(f"Removed {coin_id} from tracking")

    async def view_tracked_coins(self):
        coins = self.price_monitor.tracked_coins
        if coins:
            print("Tracked coins:")
            for coin_id, threshold in coins.items():
                current_price = await self.price_monitor.api.get_current_price(coin_id)
                if current_price is not None:
                    print(f"{coin_id}: Current Price: ${current_price:.2f}, Threshold: ${threshold:.2f}")
                    self.log_manager.log_info(f"Viewed {coin_id}: Current Price: ${current_price:.2f}, Threshold: ${threshold:.2f}")
                else:
                    print(f"{coin_id}: Unable to fetch current price, Threshold: ${threshold:.2f}")
                    self.log_manager.log_warning(f"Unable to fetch current price for {coin_id}")
        else:
            print("No coins are currently being tracked.")
            self.log_manager.log_info("Viewed tracked coins: None")

    async def view_logs(self):
        logs = self.log_manager.get_logs()
        print("Recent logs:")
        print(logs)

    async def run_simulation(self):
        coin_id = input("Enter the coin ID for simulation: ")
        days = int(input("Enter the number of days for historical data: "))
        threshold = float(input("Enter the price threshold for simulation: "))
        results = self.strategy_engine.simulate(coin_id, days, threshold)
        print("Simulation results:")
        print(results)

    async def main_loop(self):
        monitor_task = asyncio.create_task(self.price_monitor.run(interval=CHECK_INTERVAL))

        while True:
            print("\nCryptocurrency Price Tracker")
            print("1. Add coin to track")
            print("2. Remove coin from tracking")
            print("3. View tracked coins")
            print("4. View logs")
            print("5. Run simulation")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                await self.add_coin()
            elif choice == '2':
                await self.remove_coin()
            elif choice == '3':
                await self.view_tracked_coins()
            elif choice == '4':
                await self.view_logs()
            elif choice == '5':
                await self.run_simulation()
            elif choice == '6':
                print("Exiting...")
                monitor_task.cancel()
                break
            else:
                print("Invalid choice. Please try again.")

        await asyncio.gather(monitor_task, return_exceptions=True)

async def main():
    tracker = CryptoTracker()
    await tracker.main_loop()

if __name__ == "__main__":
    asyncio.run(main())