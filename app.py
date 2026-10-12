
import os
import sqlite3
from functools import wraps
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key-before-deployment"
)

# Database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "users.db")


# Connect to database
def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


# Create users table
def create_table():
    try:
        with get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

        app.logger.info("Users database initialized successfully.")

    except sqlite3.Error:
        app.logger.exception("Could not initialize users database.")
        raise


# Initialize database
create_table()


# Login protection
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Please login first.")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


# Home page
@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute(
                    """
                    INSERT INTO users (username, password)
                    VALUES (?, ?)
                    """,
                    (username, hashed_password)
                )
                conn.commit()

            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This username already exists. Please login.")
            return redirect(url_for("register"))

        except sqlite3.Error:
            app.logger.exception("Registration database error.")
            flash("Registration failed due to a database error.")
            return redirect(url_for("register"))

        except Exception:
            app.logger.exception("Unexpected registration error.")
            flash("Something went wrong. Please try again.")
            return redirect(url_for("register"))

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter username and password.")
            return redirect(url_for("login"))

        try:
            with get_db() as conn:
                user = conn.execute(
                    "SELECT * FROM users WHERE username = ?",
                    (username,)
                ).fetchone()

            if user and check_password_hash(
                user["password"], password
            ):
                session.clear()
                session["username"] = user["username"]

                flash("Login successful!")
                return redirect(url_for("home"))

            flash("Invalid username or password.")

        except sqlite3.Error:
            app.logger.exception("Login database error.")
            flash("Login failed due to a database error.")
            return redirect(url_for("login"))

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out successfully.")
    return redirect(url_for("login"))


# SOS page
@app.route("/sos")
@login_required
def sos():
    return render_template("sos.html")


# Location page
@app.route("/location")
@login_required
def location():
    return render_template("location.html")


# Emergency contacts page
@app.route("/contacts")
@login_required
def contacts():
    return render_template("contacts.html")


# Helpline page
@app.route("/help")
@login_required
def help_page():
    return render_template("help.html")


# Safety tips page
@app.route("/safety-tips")
@login_required
def safety_tips():
    return render_template("safety_tips.html")


# Friendly error logging
@app.errorhandler(500)
def internal_server_error(error):
    app.logger.exception("Internal server error: %s", error)
    return (
        "Something went wrong on the server. "
        "Please check the Render logs.",
        500
    )


if __name__ == "__main__":
    app.run(debug=True)
