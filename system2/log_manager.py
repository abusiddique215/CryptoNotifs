import logging
import json
from datetime import datetime
import pandas as pd

class LogManager:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

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

        df = pd.DataFrame(logs)
        
        # Analysis of notifications
        if 'type' in df.columns:
            notifications = df[df['type'] == 'notification']
            notifications_per_coin = notifications['coin_id'].value_counts()
            avg_price_per_coin = notifications.groupby('coin_id')['price'].mean()

            print("Notification Analysis:")
            print(f"Total notifications: {len(notifications)}")
            print("Notifications per coin:")
            print(notifications_per_coin)
            print("Average price per coin:")
            print(avg_price_per_coin)

        # Analysis of strategy simulations
        simulations = df[df['type'] == 'strategy_simulation']
        if not simulations.empty:
            simulations_per_strategy = simulations['strategy'].value_counts()
            avg_notifications_per_strategy = simulations.groupby('strategy')['notifications_count'].mean()

            print("\nStrategy Simulation Analysis:")
            print("Simulations per strategy:")
            print(simulations_per_strategy)
            print("Average notifications per strategy:")
            print(avg_notifications_per_strategy)

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