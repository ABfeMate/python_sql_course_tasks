# Currency Exchange App

This currency exchange app allows users to exchange currencies (RUB, USD, EUR) using live exchange rates obtained from the [ExchangeRate-API](https://api.exchangerate-api.com).

## Features

- Display the user's balance in RUB, USD, and EUR
- Display live exchange rates
- Allow users to buy and sell currencies
- Validate user input
- Store user balance data in a SQLite3 database

## Dependencies

- Python 3
- [requests](https://docs.python-requests.org/en/latest/)

## How to run the app

1. Install the required dependencies:

```bash
pip install requests

## **Usage**
The app will display your current balance and the live exchange rates.
Choose a currency to buy by entering its corresponding number or ticker.
Enter the amount you want to buy.
Choose a currency to sell by entering its corresponding number or ticker. (You cannot choose the same currency as the one you want to buy.)
The app will calculate the amount to sell based on the exchange rate and update your balance.
If you want to continue exchanging currencies, type 'yes'. To exit the app, type 'no'.

##**License**
This project is open-source and available under the MIT License.
