# Cryptocurrency Price Tracker

This project is a comprehensive cryptocurrency price tracking system with a notification feature. It consists of two modular systems:
1. An API endpoint that extracts real-time and historical cryptocurrency data from external sources.
2. A system that connects to this endpoint to monitor prices, generate user-defined notifications, and log all activities.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/cryptocurrency-tracker.git
   cd cryptocurrency-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure the email settings:
   Open `config.py` and update the `EMAIL_CONFIG` dictionary with your email credentials.

5. Run the main script:
   ```
   python main.py
   ```

6. Follow the prompts to enter the coin ID, price threshold, and your email address for notifications.

## Features

- Real-time price monitoring for multiple cryptocurrencies
- User-defined price thresholds for notifications
- Historical data analysis and backtesting
- Multiple notification strategies (time-based, percentage-based, custom threshold)
- Detailed logging of all activities
- Easy log export for analysis and system improvement

## Extending the System

To add support for new APIs or cryptocurrencies, modify the `system1/api_client.py` file to include new API endpoints or data sources.

## Analyzing Logs

Logs are stored in the `crypto_tracker.log` file. You can use the `LogManager.export_logs()` method to export logs for further analysis or to re-feed them into the system for optimization.

## Support

For any questions or issues, please open an issue on the GitHub repository or contact the maintainer.