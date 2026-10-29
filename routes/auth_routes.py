from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_config import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not name or not email or not password:
            flash("All fields are required", "danger")
            return redirect("/signup")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect("/signup")

        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect("/signup")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered", "danger")
            cursor.close()
            conn.close()
            return redirect("/signup")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect("/login")

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Email and password are required", "danger")
            return redirect("/login")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid email or password", "danger")
            return redirect("/login")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/login")