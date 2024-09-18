import asyncio
from system1.price_monitor import PriceMonitor
from system1.historical_data import HistoricalData
from system2.notification_manager import NotificationManager
from system2.strategy_engine import StrategyEngine
from system2.log_manager import LogManager
from user_interface import UserInterface
from config import EMAIL_CONFIG, LOG_FILE

async def main():
    log_manager = LogManager(LOG_FILE)
    price_monitor = PriceMonitor()
    historical_data = HistoricalData()
    notification_manager = NotificationManager(EMAIL_CONFIG)
    strategy_engine = StrategyEngine(historical_data)

    ui = UserInterface(price_monitor, log_manager, notification_manager, strategy_engine, historical_data)

    # Start the price monitoring in the background
    monitor_task = asyncio.create_task(run_price_monitor(price_monitor, notification_manager, log_manager, strategy_engine))

    # Run the user interface
    await ui.main_menu()

    # Cancel the monitoring task when the user exits
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass

async def run_price_monitor(price_monitor, notification_manager, log_manager, strategy_engine):
    try:
        async for coin_id, price in price_monitor.run():
            threshold = price_monitor.tracked_coins[coin_id]
            await notification_manager.notify(coin_id, price, threshold)
            log_manager.log_notification(coin_id, price, threshold, notification_manager.get_recipient(coin_id))

    except asyncio.CancelledError:
        print("Price monitoring stopped.")

if __name__ == "__main__":
    asyncio.run(main())