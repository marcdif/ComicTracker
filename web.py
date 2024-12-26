from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from utils import load_db_credentials, add_issue, remove_issue, get_publishers, get_series_titles
import mysql.connector

def web_interface():
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)

            if parsed_path.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

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

                    query = (
                        "SELECT series.publisher AS Series_Publisher, series.title AS Series_Title, books.issue AS Issue, COUNT(books.id) AS Count "
                        "FROM books "
                        "JOIN series ON books.series_fk = series.id "
                        "GROUP BY series.title, books.issue "
                        "ORDER BY series.title, books.issue;"
                    )

                    cursor.execute(query)

                    html_table = "<table border='1'>"
                    html_table += "<tr><th>Publisher</th><th>Series</th><th>Issue No.</th><th>Count</th><th>Action</th></tr>"

                    for row in cursor:
                        add_url = f"/api?action=add&publisher={row['Series_Publisher']}&series={row['Series_Title']}&issue={row['Issue']}"
                        remove_url = f"/api?action=remove&publisher={row['Series_Publisher']}&series={row['Series_Title']}&issue={row['Issue']}"
                        html_table += f"<tr><td>{row['Series_Publisher']}</td><td>{row['Series_Title']}</td><td>{row['Issue']}</td><td>{row['Count']}</td>"
                        html_table += f"<td><a href=\"{add_url}\">Add</a> | <a href=\"{remove_url}\">Remove</a></td></tr>"

                    html_table += "</table>"

                    last_publisher = query_params.get('publisher', [None])[0]
                    last_publisher = "" if last_publisher == None else f'value="{last_publisher}"'

                    last_series_title = query_params.get('series', [None])[0]
                    last_series_title = "" if last_series_title == None else f'value="{last_series_title}"'

                    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comic Book Tracker</title>
        <style>
            .form-container {{
                display: flex;
                align-items: center;
            }}
            .form-container input {{
                margin-right: 10px;
                padding: 5px;
            }}
            .form-container button {{
                padding: 5px 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <h1>Comic Book Tracker</h1>
        <form action="/api">
            <div class="form-container">
                <input type="hidden" id="action" name="action" value="add" />
                <label for="publisher">Publisher:</label>
                <input type="text" id="publisher" name="publisher" autocomplete="off" list="publisher-list" placeholder="Type publisher name" {last_publisher}>
                <datalist id="publisher-list">
                </datalist>

                <label for="series">Series:</label>
                <input type="text" id="series" name="series" autocomplete="off" list="series-list" placeholder="Type series name" {last_series_title}>
                <datalist id="series-list">
                </datalist>

                <label for="issue">Issue No:</label>
                <input type="text" id="issue" name="issue" autocomplete="off" placeholder="Issue number">
                
                <button type="submit">Submit</button>
            </div>
        </form>

        <script>
            const publisherData = {get_publishers()};

            const publisherList = document.getElementById('publisher-list');
            publisherData.forEach(publisher => {{
                const option = document.createElement('option');
                option.value = publisher;
                publisherList.appendChild(option);
            }});

            const publisherInput = document.getElementById('publisher');
            publisherInput.addEventListener('input', function() {{
                const inputValue = publisherInput.value.toLowerCase();
                const filteredpublisher = publisherData.filter(publisher => 
                    publisher.toLowerCase().includes(inputValue)
                );
                
                publisherList.innerHTML = '';
                filteredpublisher.forEach(publisher => {{
                    const option = document.createElement('option');
                    option.value = publisher;
                    publisherList.appendChild(option);
                }});
            }});

            const seriesData = {get_series_titles()};

            const seriesList = document.getElementById('series-list');
            seriesData.forEach(series => {{
                const option = document.createElement('option');
                option.value = series;
                seriesList.appendChild(option);
            }});

            const seriesInput = document.getElementById('series');
            seriesInput.addEventListener('input', function() {{
                const inputValue = seriesInput.value.toLowerCase();
                const filteredSeries = seriesData.filter(series => 
                    series.toLowerCase().includes(inputValue)
                );
                
                seriesList.innerHTML = '';
                filteredSeries.forEach(series => {{
                    const option = document.createElement('option');
                    option.value = series;
                    seriesList.appendChild(option);
                }});
            }});

            // Automatically focus on the Issue No input field when the page loads
            document.getElementById('issue').focus();
        </script>

        <h2>Comic Book Issues</h2>
        {html_table} <!-- Insert the table content here -->
    </body>
    </html>
    """

                    html = "<html><head><title>Comic Tracker</title></head><body>"
                    html += "<h1>Comic Tracker</h1>"
                    html += html_table
                    html += "</body></html>"

                    self.wfile.write(html_content.encode('utf-8'))

                except mysql.connector.Error as err:
                    self.wfile.write(f"<p>Error: {err}</p>".encode('utf-8'))

                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()

            elif parsed_path.path == '/api':
                action = query_params.get('action', [None])[0]
                publisher = query_params.get('publisher', [None])[0]
                series = query_params.get('series', [None])[0]
                issue = query_params.get('issue', [None])[0]

                if not action or not series or not issue:
                    self.send_response(400)
                    self.end_headers()
                    return

                try:
                    issue_number = int(issue)
                    if action == 'add':
                        add_issue(publisher, series, issue_number)
                    elif action == 'remove':
                        remove_issue(publisher, series, issue_number)
                    else:
                        self.send_response(400)
                        self.end_headers()
                        return

                    self.send_response(302)
                    self.send_header('Location', f'/?publisher={publisher}&series={series}')
                    self.end_headers()

                except ValueError:
                    self.send_response(400)
                    self.end_headers()

            else:
                self.send_response(404)
                self.end_headers()

    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Web server running on port 8080... Press Ctrl+C to stop.")
    httpd.serve_forever()
