# StudyTrack — Student Assignment & Deadline Tracker

A beginner-friendly mini-project prototype built with Python, Flask, HTML, CSS and SQLite.

## Features
- Add assignments with title, subject, due date and optional description
- View assignment dashboard with total, pending, completed and overdue counts
- Mark an assignment completed or reopen it
- Edit assignment details
- Delete assignments
- Automatically label unfinished assignments whose due dates have passed as overdue
- Persist data in a local SQLite database

## Requirements
- Python 3.9 or later
- pip

## Run locally
1. Unzip the project and open a terminal in this folder.
2. Create a virtual environment (recommended):
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the app: `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.

The SQLite database file `assignments.db` is created automatically the first time the app runs.

## Viva explanation in one minute
HTML builds the page and forms. CSS styles the dashboard. Flask receives form submissions and maps URLs to Python functions. SQLite stores assignments in a table. When the home page is requested, Flask reads the rows, calculates the summary counts and determines which unfinished tasks are overdue by comparing their due date with today's date.

## Important notes
- This is a local academic prototype, not a production-ready multi-user service.
- Before public deployment, change the Flask secret key, disable debug mode, add authentication and strengthen validation/security.
- The first run needs an internet connection only if the Google Fonts import in the stylesheet is to load; the application itself works without it.
