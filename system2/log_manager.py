import logging
import json
from datetime import datetime
from collections import defaultdict

class LogManager:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def log_api_connection(self, success, details):
        log_entry = {
            "type": "api_connection",
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_entry))

    def log_notification(self, coin_id, price, threshold, recipient):
        log_entry = {
            "type": "notification",
            "coin_id": coin_id,
            "price": price,
            "threshold": threshold,
            "recipient": recipient,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_entry))

    def log_strategy_simulation(self, strategy, coin_id, params, notifications_count):
        log_entry = {
            "type": "strategy_simulation",
            "strategy": strategy,
            "coin_id": coin_id,
            "params": params,
            "notifications_count": notifications_count,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_entry))

    def export_logs(self, output_file):
        with open(self.log_file, 'r') as log_file, open(output_file, 'w') as out_file:
            for line in log_file:
                out_file.write(line)

    def get_recent_logs(self, n=10):
        with open(self.log_file, 'r') as log_file:
            logs = log_file.readlines()
            return logs[-n:]

    def analyze_logs(self):
        logs = []
        with open(self.log_file, 'r') as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line.split(' - ')[-1])
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    continue

        notifications = [log for log in logs if log['type'] == 'notification']
        simulations = [log for log in logs if log['type'] == 'strategy_simulation']

        # Analysis of notifications
        notifications_per_coin = defaultdict(int)
        total_price_per_coin = defaultdict(float)
        for notification in notifications:
            coin_id = notification['coin_id']
            notifications_per_coin[coin_id] += 1
            total_price_per_coin[coin_id] += notification['price']

        print("Notification Analysis:")
        print(f"Total notifications: {len(notifications)}")
        print("Notifications per coin:")
        for coin_id, count in notifications_per_coin.items():
            print(f"{coin_id}: {count}")
        print("Average price per coin:")
        for coin_id, total_price in total_price_per_coin.items():
            avg_price = total_price / notifications_per_coin[coin_id]
            print(f"{coin_id}: ${avg_price:.2f}")

        # Analysis of strategy simulations
        simulations_per_strategy = defaultdict(int)
        total_notifications_per_strategy = defaultdict(int)
        for simulation in simulations:
            strategy = simulation['strategy']
            simulations_per_strategy[strategy] += 1
            total_notifications_per_strategy[strategy] += simulation['notifications_count']

        print("\nStrategy Simulation Analysis:")
        print("Simulations per strategy:")
        for strategy, count in simulations_per_strategy.items():
            print(f"{strategy}: {count}")
        print("Average notifications per strategy:")
        for strategy, total_notifications in total_notifications_per_strategy.items():
            avg_notifications = total_notifications / simulations_per_strategy[strategy]
            print(f"{strategy}: {avg_notifications:.2f}")

    def re_feed_logs(self, price_monitor, notification_manager):
        with open(self.log_file, 'r') as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line.split(' - ')[-1])
                    if log_entry['type'] == 'notification':
                        price_monitor.add_coin(log_entry['coin_id'], log_entry['threshold'])
                        notification_manager.add_notification(log_entry['coin_id'], log_entry['recipient'])
                except json.JSONDecodeError:
                    continue
        print("Logs re-fed into the system.")

    def get_logs(self, num_lines=50):
        try:
            with open(self.log_file, 'r') as file:
                lines = file.readlines()
                return ''.join(lines[-num_lines:])
        except Exception as e:
            return f"Error reading log file: {str(e)}"

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)