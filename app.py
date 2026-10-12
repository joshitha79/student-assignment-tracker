from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-before-deployment"
DB_PATH = Path(__file__).with_name("assignments.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN ('Pending', 'Completed'))
            )
        """)

@app.route("/")
def index():
    today = date.today().isoformat()
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM assignments ORDER BY "
            "CASE WHEN status = 'Completed' THEN 1 ELSE 0 END, due_date ASC, id DESC"
        ).fetchall()
    assignments = []
    for row in rows:
        item = dict(row)
        item["overdue"] = item["status"] != "Completed" and item["due_date"] < today
        assignments.append(item)
    stats = {
        "total": len(assignments),
        "pending": sum(a["status"] == "Pending" for a in assignments),
        "completed": sum(a["status"] == "Completed" for a in assignments),
        "overdue": sum(a["overdue"] for a in assignments),
    }
    return render_template("index.html", assignments=assignments, stats=stats, today=today)

@app.route("/add", methods=["POST"])
def add_assignment():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip()
    if not title or not subject or not due_date:
        flash("Please fill in the title, subject and due date.", "error")
        return redirect(url_for("index"))
    try:
        date.fromisoformat(due_date)
    except ValueError:
        flash("Please enter a valid due date.", "error")
        return redirect(url_for("index"))
    with get_db() as conn:
        conn.execute(
            "INSERT INTO assignments (title, subject, description, due_date) VALUES (?, ?, ?, ?)",
            (title, subject, description, due_date)
        )
    flash("Assignment added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/<int:assignment_id>/toggle", methods=["POST"])
def toggle_assignment(assignment_id):
    with get_db() as conn:
        row = conn.execute("SELECT status FROM assignments WHERE id = ?", (assignment_id,)).fetchone()
        if row:
            new_status = "Completed" if row["status"] == "Pending" else "Pending"
            conn.execute("UPDATE assignments SET status = ? WHERE id = ?", (new_status, assignment_id))
    return redirect(url_for("index"))

@app.route("/<int:assignment_id>/delete", methods=["POST"])
def delete_assignment(assignment_id):
    with get_db() as conn:
        conn.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
    flash("Assignment deleted.", "success")
    return redirect(url_for("index"))

@app.route("/<int:assignment_id>/edit", methods=["POST"])
def edit_assignment(assignment_id):
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip()
    if not title or not subject or not due_date:
        flash("Title, subject and due date are required.", "error")
        return redirect(url_for("index"))
    try:
        date.fromisoformat(due_date)
    except ValueError:
        flash("Please enter a valid due date.", "error")
        return redirect(url_for("index"))
    with get_db() as conn:
        conn.execute(
            "UPDATE assignments SET title=?, subject=?, description=?, due_date=? WHERE id=?",
            (title, subject, description, due_date, assignment_id)
        )
    flash("Assignment updated.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
