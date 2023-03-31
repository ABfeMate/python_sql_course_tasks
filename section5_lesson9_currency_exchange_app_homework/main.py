# For this task I decided to use https://api.exchangerate-api.com API to get live currency exchange rates
import sqlite3
import requests

"""Connecting to a db"""
db_connection = sqlite3.connect("exchanger.db")
cursor = db_connection.cursor()

"""Creating users_balance table"""
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_balance(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Balance_RUB REAL NOT NULL,
    Balance_USD REAL NOT NULL,
    Balance_EUR REAL NOT NULL);
""")
db_connection.commit()

"""Adding initial user to the database."""
# The user has 100000 RUB, 1000 USD and 1000 EUR initially.
initial_user = (1, 100000, 1000, 1000)
cursor.execute("""
    INSERT OR IGNORE INTO users_balance(UserID, Balance_RUB, Balance_USD, Balance_EUR)
    -- IGNORE means that user will be added only if it doesn't exist
    -- I explicitly add UserId, so new user would not be added each time application runs
    VALUES(?,?,?,?);""", initial_user)
print("Adding initial user data to the table...")
db_connection.commit()

"""FUNCTIONS"""


# creating a function to ask user to choose a currency for operation and validate user's input
def get_currency_choice(action):
    """Asks users to choose a currency and validates users` input."""
    if action == "buy":
        currency_choice_prompt = "\nChoose currency you would like to buy:\n1. RUB\n2. USD \n3. EUR\n"
    elif action == "sell":
        currency_choice_prompt = "\nChoose currency you would like to sell:\n1. RUB\n2. USD \n3. EUR\n"
    currency_dict = {
        "1": "RUB",
        "2": "USD",
        "3": "EUR",
        "RUB": "RUB",
        "USD": "USD",
        "EUR": "EUR"
    }

    while True:
        """Validates users` input(only numbers or currency tickers are allowed)."""
        choice = input(currency_choice_prompt).upper()
        if choice in currency_dict:
            return currency_dict[choice]
        else:
            print("There is no such currency. Enter a number or a currency ticker.")


# Creating a function that gets live data from an API
def get_currency_data(currency):
    """Gets currency exchange rates from exchangerate API relative to the currency provided as an argument."""
    base_url = "https://api.exchangerate-api.com/v4/latest/"
    response = requests.get(f"{base_url}{currency}")
    data = response.json()
    rates = data["rates"]
    return rates


def get_amount():
    """Asks the user for the amount they want to buy and validates their input."""
    # I implemented a validation, so users can only enter positive number
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount > 0:
                return amount
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_balance():
    """Fetches and displays the user's balance for each currency."""
    cursor.execute("SELECT Balance_RUB, Balance_USD, Balance_EUR FROM users_balance LIMIT 1;")
    balance_rub, balance_usd, balance_eur = cursor.fetchone()

    print("\nYour current balance is:")
    print(f"RUB: {balance_rub:.2f}")
    print(f"USD: {balance_usd:.2f}")
    print(f"EUR: {balance_eur:.2f}\n")


"""MAIN APP"""
while True:
    print("\n*** Welcome to our currency exchange office! ***")

    display_balance()

    print("The exchange rate is as follows: ")
    print(f"1 USD = {get_currency_data('USD')['RUB']} RUB")
    print(f"1 EUR = {get_currency_data('EUR')['RUB']} RUB")
    print(f"1 USD = {get_currency_data('USD')['EUR']} EUR")
    print(f"1 EUR = {get_currency_data('EUR')['USD']} EUR")

    # asking users which currency they want to buy
    currency_to_buy = get_currency_choice("buy")

    # connecting the exchange rate API to get up-to-date data of the currency exchange rates
    exchange_rates = get_currency_data(currency_to_buy)

    # asking users how much they want to buy
    amount_to_buy = get_amount()

    # asking users which currency they want to sell
    while True:
        currency_to_sell = get_currency_choice("sell")
        if currency_to_sell == currency_to_buy:
            print("*** You cannot choose the same currency for both operations. Try again. ***")
            continue
        break

    # calculating the amount to receive based on the exchange rate
    amount_to_sell = amount_to_buy * exchange_rates[currency_to_sell]

    # getting the balance of the currency to sell
    cursor.execute(f"""SELECT Balance_{currency_to_sell} FROM users_balance LIMIT 1;""")
    balance_currency_to_sell = cursor.fetchone()[0]

    # getting the balance of the currency to buy
    cursor.execute(f"""SELECT Balance_{currency_to_buy} FROM users_balance LIMIT 1;""")
    balance_currency_to_buy = cursor.fetchone()[0]

    # checking if user has enough money
    if amount_to_sell < balance_currency_to_sell:
        new_balance_currency_to_sell = balance_currency_to_sell - amount_to_sell
        new_balance_currency_to_sell = float(f"{new_balance_currency_to_sell:.2f}")

        new_balance_currency_to_buy = balance_currency_to_buy + amount_to_buy
        new_balance_currency_to_buy = float(f"{new_balance_currency_to_buy:.2f}")

        cursor.execute(f"""UPDATE users_balance SET Balance_{currency_to_sell} = ?, Balance_{currency_to_buy} = ?;
        """, (new_balance_currency_to_sell, new_balance_currency_to_buy))
        db_connection.commit()
        print(
            f"Your balance has been updated.\nYou have bought {amount_to_buy:.2f} {currency_to_buy} with {amount_to_sell:.2f} {currency_to_sell}")
    else:
        print(f"You don't have enough {currency_to_sell}")

    continue_exchange = input("\nWould you like to continue exchanging currency?(yes/no): ")
    if continue_exchange == "no":
        break
