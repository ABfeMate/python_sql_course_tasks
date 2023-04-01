import sqlite3

"""Creating a connection"""
db_connection = sqlite3.connect("registration.db")
cursor = db_connection.cursor()

"""Creating users_data table and adding new user"""
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL UNIQUE,
    Password  TEXT NOT NULL,
    Code INTEGER NOT NULL,
    Logged_in BOOLEAN NOT NULL
    );

    INSERT OR IGNORE INTO users_data(Login, Password, Code, Logged_in)
    VALUES('Ivan', 'qwer1234', 1234, 0);""")
db_connection.commit()


def get_limited_input(input_type, max_length, prompt):
    """limits user's input to a certain length"""
    while True:
        user_input = input(prompt)
        if len(user_input) <= 3:
            print(f"The {input_type} is shorter than 4 symbols. Try again.")
            continue
        if len(user_input) <= max_length:
            return user_input
        else:
            print(f"{input_type.capitalize()} is too long! Max length is {max_length} symbols. Try again.")


def create_new_user():
    """creates new user, ads it to the database"""
    while True:
        login = get_limited_input("login", 12, "Create your login (min length - 4, max length - 12): ")
        cursor.execute("""SELECT 1 FROM users_data WHERE Login = ?""", (login,))
        if cursor.fetchone() is not None:
            print("This login is already in use. Try another one.")
            continue
        password = get_limited_input("password", 26, "Create your password (min length - 4, max length - 26): ")
        try:
            secret_code = int(get_limited_input("secret code", 4, "Create your secret code (4 digits): "))
        except ValueError:
            print("Only enter numbers for the secret code.")
            continue

        data = (login, password, int(secret_code))
        cursor.execute("""INSERT INTO users_data(Login, Password, Code, Logged_in) VALUES (?,?,?,0);""", data)
        break

    print("You have successfully created a new user account!")
    db_connection.commit()


def log_in():
    """logs into the database"""
    login = input("Enter your login: ")
    password = input("Enter your password: ")
    cursor.execute("""SELECT 1 FROM users_data WHERE Login = ? AND Password = ?""", (login, password))
    db_connection.commit()

    if cursor.fetchone() is not None:
        print("You have successfully logged in!")
        cursor.execute("""UPDATE users_data SET Logged_in = ? WHERE Login = ?""", (1, login))
        db_connection.commit()
        return login
    else:
        print("You've entered the wrong credentials.")
        return None


def log_out(current_user):
    """Logs out the user."""
    cursor.execute("""UPDATE users_data SET Logged_in = ? WHERE Login = ?""", (0, current_user))
    db_connection.commit()
    print("You have successfully logged out!")
    return None


def reset_password():
    """resets the password"""
    login = input("Enter your login: ")
    secret_code = input("Enter your secret code (4 digits): ")
    cursor.execute("""SELECT 1 FROM users_data WHERE Login = ? AND Code = ?""", (login, int(secret_code)))
    if cursor.fetchone() is not None:
        new_password = input("Enter new password: ")
        cursor.execute("""UPDATE users_data SET Password = ? WHERE Login = ?""", (new_password, login))
        db_connection.commit()
        print(f"Password of the user {login} has been updated.")
    else:
        print("You've entered the wrong credentials.")


def initialize_users():
    """Checks for logged-in users and sets the current user if there's only one logged in."""
    cursor.execute("SELECT Login FROM users_data WHERE Logged_in = 1")
    logged_in_users = cursor.fetchall()

    if len(logged_in_users) > 1:
        print("More than one user is logged in. Logging out all users.")
        cursor.execute("UPDATE users_data SET Logged_in = 0")
        db_connection.commit()
        return None
    elif len(logged_in_users) == 1:
        # print(f"User {logged_in_users[0][0]} is currently logged in.")
        return logged_in_users[0][0]
    else:
        return None


def show_options(current_user):
    """Allows users to choose options based on the current user's login status"""
    if current_user is None:
        choice = input("\nTo sign up enter '1', to log in enter '2', to reset password enter '3', to exit enter '4': ")
        if choice == "1":
            create_new_user()
        elif choice == "2":
            current_user = log_in()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            return "exit"
        else:
            print("Invalid input. Please enter '1', '2', '3', or '4'.")
    else:
        print(f"You are currently logged in as {current_user}")
        choice = input("\nTo log out enter '1', to reset password enter '2', to exit enter '3': ")
        if choice == "1":
            current_user = log_out(current_user)
        elif choice == "2":
            reset_password()
        elif choice == "3":
            return "exit"
        else:
            print("Invalid input. Please enter '1', '2', or '3'.")
    return current_user


current_user = initialize_users()
while True:
    current_user = show_options(current_user)
    if current_user == "exit":
        if current_user is not None and current_user != "exit":
            current_user = log_out(current_user)
        break
