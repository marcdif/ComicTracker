ComicTracker
===

A simple Python program that uses a MySQL/MariaDB database as a backend to catalog a comic book collection.

The program has several operating modes, all of which complete one transaction before exiting, except the web interface.
```
Usage: python main.py <function> [arguments]
Functions: add_issue, remove_issue, clear_issue, view_all_series, view_all_issues, web_interface, get_publishers, get_series_titles
```
- `add_issue <publisher> <series_title> <issue_number> <box>` - Add a new issue.
- `remove_issue <publisher> <series_title> <issue_number>` - Remove one copy of an existing issue.
- `clear_issue <publisher> <series_title> <issue_number>` - Remove all copies of an existing issue.
- `view_all_series` - Print all series, their publishers, and how many issues are present for each series.
- `view_all_issues` - Print a detailed breakdown of all issues, which series/publisher they belong to, how many copies there are of it, and what box it's in.
- `web_interface` - Start a web server that displays the `view_all_issues` output in an HTML table (shown below) along with actions that add/remove/clear issues using the other functions of the program.
- `get_publishers` - Get a list of all publishers in the database, returned in Python list/JavaScript array format.
- `get_series_titles` - Get a list of all series titles in the database, returned in Python list/JavaScript array format.

Web Interface:
---
![image](https://github.com/user-attachments/assets/03272145-37be-478b-87e6-bd47333a1ce3)

Installation:
---
1. Install/configure MySQL (or MongoDB) database. The database schema is provided in the `database_schema.sql` file
2. Prepare a `db_secret.json` file or provide the database credentials in environment variables (explained below).
3. Start the application! It should be that simple.

Database Credentials:
---

db_secret.json:
```
{
    "host": "your-database-ip-here",
    "user": "your-username-here",
    "password": "your-password-here"
}
```

Environment Variables:
- `DB_HOST` - your database IP address
- `DB_USER` - your database username
- `DB_PASSWORD` - your database password
