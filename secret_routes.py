from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import db, SecretMessage, ViewAttempt
from crypto_service import CryptoService

secret = Blueprint("secret", __name__)


def _get_crypto() -> CryptoService:
    """Instancia CryptoService con la clave de la app (equivalente a @Autowired)."""
    return CryptoService(current_app.config["FERNET_KEY"])


# ─── GET /  →  home con historial ─────────────────────────────────────────────
@secret.route("/")
@login_required
def home():
    # Mensajes cifrados propios ordenados por fecha descendente
    my_messages = (SecretMessage.query
                   .filter_by(owner_id=current_user.id)
                   .order_by(SecretMessage.created_at.desc())
                   .all())

    # Historial de intentos de descifrado propios
    my_attempts = (ViewAttempt.query
                   .filter_by(viewer_id=current_user.id)
                   .order_by(ViewAttempt.attempted_at.desc())
                   .all())

    return render_template("home.html",
                           my_messages=my_messages,
                           my_attempts=my_attempts)


# ─── POST /encrypt  ───────────────────────────────────────────────────────────
@secret.route("/encrypt", methods=["POST"])
@login_required
def encrypt():
    plain_text = request.form.get("text", "").strip()

    if not plain_text:
        flash("El texto no puede estar vacío.", "danger")
        return redirect(url_for("secret.home"))

    crypto = _get_crypto()
    result = crypto.encrypt(plain_text)

    message = SecretMessage(
        token          = result.token,
        encrypted_text = result.encrypted_text,
        original_text  = plain_text,
        owner_id       = current_user.id,
    )
    db.session.add(message)
    db.session.commit()

    flash(f"Texto cifrado. Tu token es: {result.token}", "success")
    return redirect(url_for("secret.home"))


# ─── POST /decrypt  ───────────────────────────────────────────────────────────
@secret.route("/decrypt", methods=["POST"])
@login_required
def decrypt():
    token = request.form.get("token", "").strip()

    if not token:
        flash("Debes ingresar un token.", "danger")
        return redirect(url_for("secret.home"))

    # Buscar el mensaje por token (solo del usuario actual)
    message = SecretMessage.query.filter_by(token=token).first()

    if not message or message.owner_id != current_user.id:
        # Registrar intento fallido
        attempt = ViewAttempt(
            token_used        = token,
            original_text     = None,
            successful        = False,
            viewer_id         = current_user.id,
            secret_message_id = None,
        )
        db.session.add(attempt)
        db.session.commit()
        flash("Token inválido o no tienes permiso para verlo.", "danger")
        return redirect(url_for("secret.home"))

    # Descifrar
    crypto         = _get_crypto()
    decrypted_text = crypto.decrypt(message.encrypted_text)

    # Registrar intento exitoso
    attempt = ViewAttempt(
        token_used        = token,
        original_text     = decrypted_text,
        successful        = True,
        viewer_id         = current_user.id,
        secret_message_id = message.id,
    )
    db.session.add(attempt)
    db.session.commit()

    flash(f'Texto descifrado: "{decrypted_text}"', "success")
    return redirect(url_for("secret.home"))
