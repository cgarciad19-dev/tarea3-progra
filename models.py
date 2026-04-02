from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ─── Equivalente a @Entity User ───────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones (equivalente a @OneToMany)
    messages = db.relationship("SecretMessage", back_populates="owner",
                               cascade="all, delete-orphan", lazy="dynamic")
    attempts = db.relationship("ViewAttempt",   back_populates="viewer",
                               cascade="all, delete-orphan", lazy="dynamic")

    def get_id(self):           # requerido por Flask-Login
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"


# ─── Equivalente a @Entity SecretMessage ──────────────────────────────────────
class SecretMessage(db.Model):
    __tablename__ = "secret_messages"

    id             = db.Column(db.Integer, primary_key=True)
    token          = db.Column(db.String(36), unique=True, nullable=False, index=True)
    encrypted_text = db.Column(db.Text, nullable=False)
    original_text  = db.Column(db.Text, nullable=False)   # guardado para historial
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # FK al dueño
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner    = db.relationship("User", back_populates="messages")

    # Intentos de descifrado sobre este mensaje
    view_attempts = db.relationship("ViewAttempt", back_populates="secret_message",
                                    cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<SecretMessage token={self.token}>"


# ─── Equivalente a @Entity ViewAttempt ────────────────────────────────────────
class ViewAttempt(db.Model):
    __tablename__ = "view_attempts"

    id            = db.Column(db.Integer, primary_key=True)
    token_used    = db.Column(db.String(36), nullable=False)
    original_text = db.Column(db.Text, nullable=True)   # None si el token era inválido
    attempted_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    successful    = db.Column(db.Boolean, default=False)

    # FK al usuario que intentó descifrar
    viewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    viewer    = db.relationship("User", back_populates="attempts")

    # FK al mensaje (puede ser None si el token no existía)
    secret_message_id = db.Column(db.Integer, db.ForeignKey("secret_messages.id"),
                                  nullable=True)
    secret_message    = db.relationship("SecretMessage", back_populates="view_attempts")

    def __repr__(self):
        return f"<ViewAttempt token={self.token_used} ok={self.successful}>"
