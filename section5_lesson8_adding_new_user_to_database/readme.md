This is my solution to a homework task from the [Python and SQLite Course by Alex Smith](https://stepik.org/course/134773/info).

# User Registration System
This is a simple command-line user registration system built using Python and SQLite. Users can sign up, log in, log out, and reset their passwords.

## Features
Users can sign up with a unique login, password, and a 4-digit secret code.
Users can log in with their login and password.
Users can log out.
Users can reset their password using their login and secret code.

## Technical Details
This project uses SQLite to store user data. The database has a single table called users_data with the following schema:

CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL UNIQUE,
    Password  TEXT NOT NULL,
    Code INTEGER NOT NULL,
    Logged_in BOOLEAN NOT NULL
);

The database is created and managed using Python's built-in sqlite3 module.

## License
This project is open source and available under the MIT License.
