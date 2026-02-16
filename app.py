from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "neural_kavach_secret"

# ================= DATABASE INIT =================

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)

    # Scan history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            type TEXT,
            input TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        session["user"] = email
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT type, input, status, timestamp FROM scan_history ORDER BY id DESC LIMIT 10")
    history = c.fetchall()
    conn.close()

    return render_template("dashboard.html", history=history)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

# ================= EMAIL CHECK =================

@app.route("/check_email", methods=["POST"])
def check_email():
    email = request.form["email"]
    breached = ["test@gmail.com", "admin@gmail.com"]

    status = "BREACHED" if email in breached else "SAFE"

    save_scan("Email", email, status)
    return jsonify({"status": status})

# ================= URL CHECK =================

@app.route("/check_url", methods=["POST"])
def check_url():
    url = request.form["url"].lower()
    score = 0

    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        score += 1
    if "@" in url:
        score += 1
    if len(url) > 75:
        score += 1

    status = "PHISHING RISK" if score >= 2 else "SAFE"

    save_scan("URL", url, status)
    return jsonify({"status": status})

# ================= SAVE SCAN =================

def save_scan(scan_type, user_input, status):
    if "user" not in session:
        return

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO scan_history (user, type, input, status, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user"],
        scan_type,
        user_input,
        status,
        datetime.now().strftime("%d %b %Y %H:%M")
    ))
    conn.commit()
    conn.close()

# ================= REPORT SYSTEM =================

@app.route("/report", methods=["POST"])
def report():
    rtype = request.form["type"]
    content = request.form["content"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports (type, content, timestamp)
        VALUES (?, ?, ?)
    """, (
        rtype,
        content,
        datetime.now().strftime("%d %b %Y %H:%M")
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})

# ================= ADMIN PANEL =================

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY id DESC")
    reports = c.fetchall()
    conn.close()

    return render_template("admin.html", reports=reports)

# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)
