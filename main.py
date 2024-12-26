from utils import add_issue, remove_issue, view_all_issues, view_all_series, get_publishers, get_series_titles
from web import web_interface
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <function> [arguments]")
        print("Functions: add_issue, remove_issue, view_all_series, view_all_issues, web_interface, get_publishers, get_series_titles")
        return

    command = sys.argv[1]

    if command == 'add_issue':
        if len(sys.argv) != 5:
            print("Usage: python main.py add_issue <publisher> <series_title> <issue_number>")
            return
        publisher = sys.argv[2]
        series_title = sys.argv[3]
        issue_number = int(sys.argv[4])
        add_issue(publisher, series_title, issue_number)

    elif command == 'remove_issue':
        if len(sys.argv) != 5:
            print("Usage: python main.py remove_issue <publisher> <series_title> <issue_number>")
            return
        pubisher = sys.argv[2]
        series_title = sys.argv[3]
        issue_number = int(sys.argv[4])
        remove_issue(publisher, series_title, issue_number)

    elif command == 'view_all_series':
        view_all_series()

    elif command == 'view_all_issues':
        view_all_issues()

    elif command == 'web_interface':
        web_interface()

    elif command == 'get_publishers':
        print(f"{get_publishers()}")

    elif command == 'get_series_titles':
        print(f"{get_series_titles()}")

    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
