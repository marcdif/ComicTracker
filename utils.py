import os
import json
import mysql.connector

def load_db_credentials():
    if os.path.exists('db_secret.json'):
        with open('db_secret.json', 'r') as secret_file:
            return json.load(secret_file)

    return {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD')
    }

def add_issue(publisher, series_title, issue_number, box):
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor()

        # Check if the series exists
        cursor.execute("SELECT id FROM series WHERE title = %s AND publisher = %s", (series_title, publisher,))
        series = cursor.fetchone()

        if not series:
            # Create new series if it doesn't exist
            cursor.execute("INSERT INTO series (title, publisher) VALUES (%s, %s)", (series_title, publisher,))
            connection.commit()
            series_id = cursor.lastrowid
        else:
            series_id = series[0]

        cursor.execute("SELECT box FROM books WHERE series_fk = %s AND issue = %s LIMIT 1", (series_id, issue_number))
        existing_box = cursor.fetchone()

        if existing_box:
            existing_box_letter = existing_box[0]
            if existing_box_letter and existing_box_letter != box:
                print(f"Error: {series_title} #{issue_number} already in Box {existing_box_letter}, same issue can't be present in multiple boxes")
                return

        # Insert the new issue into books
        cursor.execute("INSERT INTO books (series_fk, issue, box) VALUES (%s, %s, %s)", (series_id, issue_number, box))
        connection.commit()

        print(f"Issue No. {issue_number} added to series '{series_title}' in Box {box}.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def remove_issue(publisher, series_title, issue_number):
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor()

        # Find the series ID
        cursor.execute("SELECT id FROM series WHERE title = %s AND publisher = %s", (series_title, publisher,))
        series = cursor.fetchone()

        if not series:
            print(f"Series '{series_title}' not found.")
            return

        series_id = series[0]

        # Remove one instance of the issue
        cursor.execute("DELETE FROM books WHERE series_fk = %s AND issue = %s LIMIT 1", (series_id, issue_number))
        if cursor.rowcount == 0:
            print(f"Issue No. {issue_number} not found in series '{series_title}'.")
            return

        connection.commit()

        # Check if the series has any remaining issues
        cursor.execute("SELECT COUNT(*) FROM books WHERE series_fk = %s", (series_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Delete the series if no issues remain
            cursor.execute("DELETE FROM series WHERE id = %s", (series_id,))
            connection.commit()
            print(f"Series '{series_title}' deleted as it has no remaining issues.")
        else:
            print(f"One copy of Issue No. {issue_number} removed from series '{series_title}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def clear_issue(publisher, series_title, issue_number):
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor()

        # Find the series ID
        cursor.execute("SELECT id FROM series WHERE title = %s AND publisher = %s", (series_title, publisher,))
        series = cursor.fetchone()

        if not series:
            print(f"Series '{series_title}' not found.")
            return

        series_id = series[0]

        # Remove all instances of the issue
        cursor.execute("DELETE FROM books WHERE series_fk = %s AND issue = %s", (series_id, issue_number))
        if cursor.rowcount == 0:
            print(f"Issue No. {issue_number} not found in series '{series_title}'.")
            return

        connection.commit()

        # Check if the series has any remaining issues
        cursor.execute("SELECT COUNT(*) FROM books WHERE series_fk = %s", (series_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Delete the series if no issues remain
            cursor.execute("DELETE FROM series WHERE id = %s", (series_id,))
            connection.commit()
            print(f"Series '{series_title}' deleted as it has no remaining issues.")
        else:
            print(f"All copies of Issue No. {issue_number} removed from series '{series_title}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_publishers():
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all series and their issue counts
        query = (
            "SELECT series.publisher AS Series_Publisher "
            "FROM series "
            "GROUP BY series.publisher;"
        )

        cursor.execute(query)

        publishers = []

        for row in cursor:
            publishers.append(row['Series_Publisher'])
        
        return publishers

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_series_titles():
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all series and their issue counts
        query = (
            "SELECT series.title AS Series_Title "
            "FROM series;"
        )

        cursor.execute(query)

        series_titles = []

        for row in cursor:
            series_titles.append(row['Series_Title'])
        
        return series_titles

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_all_series():
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all series and their issue counts
        query = (
            "SELECT series.publisher AS Series_Publisher, series.title AS Series_Title, COUNT(books.id) AS Issue_Count "
            "FROM series "
            "LEFT JOIN books ON series.id = books.series_fk "
            "GROUP BY series.title "
            "ORDER BY series.publisher, series.title;"
        )

        cursor.execute(query)

        print(f"{'Publisher':<30} {'Series':<40} {'Issue Count':<10}")
        print("-" * 40)

        for row in cursor:
            print(f"{row['Series_Publisher']:<30} {row['Series_Title']:<40} {row['Issue_Count']:<10}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_all_issues():
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all issues
        query = (
            "SELECT series.publisher AS Series_Publisher, series.title AS Series_Title, books.issue AS Issue, COUNT(books.id) AS Count, books.box AS Box "
            "FROM books "
            "JOIN series ON books.series_fk = series.id "
            "GROUP BY series.title, books.issue "
            "ORDER BY series.publisher, series.title, books.issue;"
        )

        cursor.execute(query)

        print(f"{'Publisher':<30} {'Series':<40} {'Issue No.':<10} {'Count':<5} {'Box':<3}")
        print("-" * 50)

        for row in cursor:
            print(f"{row['Series_Publisher']:<30} {row['Series_Title']:<40} {row['Issue']:<10} {row['Count']:<5} {row['Box']:<3}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_issues_count():
    db_credentials = load_db_credentials()
    try:
        connection = mysql.connector.connect(
            host=db_credentials['host'],
            user=db_credentials['user'],
            password=db_credentials['password'],
            database='comictracker',
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all issues
        query = (
            "SELECT COUNT(books.id) AS Count "
            "FROM books;"
        )

        cursor.execute(query)

        for row in cursor:
            return row['Count']

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
