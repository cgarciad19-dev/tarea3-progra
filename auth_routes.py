from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from user_service import UserService

auth = Blueprint("auth", __name__)


# ─── GET /register  ───────────────────────────────────────────────────────────
@auth.route("/register", methods=["GET"])
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for("secret.home"))
    return render_template("register.html")


# ─── POST /register  ──────────────────────────────────────────────────────────
@auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm  = request.form.get("confirm_password", "")

    # Validaciones básicas (equivalente a BindingResult)
    if not username or not email or not password:
        flash("Todos los campos son obligatorios.", "danger")
        return render_template("register.html"), 400

    if password != confirm:
        flash("Las contraseñas no coinciden.", "danger")
        return render_template("register.html"), 400

    if len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        return render_template("register.html"), 400

    try:
        user = UserService.register(username, email, password)
        login_user(user)
        flash(f"¡Bienvenido, {user.username}!", "success")
        return redirect(url_for("secret.home"))
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("register.html"), 400


# ─── GET /login  ──────────────────────────────────────────────────────────────
@auth.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("secret.home"))
    return render_template("login.html")


# ─── POST /login  ─────────────────────────────────────────────────────────────
@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = UserService.find_by_username(username)
    if not user or not UserService.verify_password(user, password):
        flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("login.html"), 401

    login_user(user, remember=True)
    flash(f"¡Bienvenido de vuelta, {user.username}!", "success")
    next_page = request.args.get("next")
    return redirect(next_page or url_for("secret.home"))


# ─── POST /logout  ────────────────────────────────────────────────────────────
@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))
