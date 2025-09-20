from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="secinfo",
        autocommit=True
    )

app = Flask(__name__)
app.secret_key = "dev-secret"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        db = get_db()
        cursor = db.cursor(dictionary=True, buffered=True)
        query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        finally:
            cursor.close()
            db.close()
        row = None
        if rows:
            base_username = username.split("'")[0] if "'" in username else username
            preferred_rows = [r for r in rows if r.get("username") == base_username]
            if preferred_rows:
                row = preferred_rows[0]
            else:
                admin_rows = [r for r in rows if r.get("username") == "admin"]
                row = admin_rows[0] if admin_rows else rows[0]
        if row:
            session["username"] = row["username"]
            session["role"] = row["role"]
            return redirect(url_for("role"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password required")
            return render_template("register.html")
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
            count = cursor.fetchone()[0]
            if count > 0:
                flash("Username already exists")
                return render_template("register.html")
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, "user"))
        finally:
            cursor.close()
            db.close()
        flash("Registered successfully. Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/role")
def role():
    role = session.get("role")
    if not role:
        return redirect(url_for("login"))
    return render_template("role.html", role=role)


