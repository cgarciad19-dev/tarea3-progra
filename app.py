import os
from flask import Flask
from models import db
from user_service import init_login_manager
from auth_routes import auth
from secret_routes import secret
from crypto_service import CryptoService


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Configuración (equivalente a application.properties) ─────────────────
    app.config["SECRET_KEY"]    = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///tokenvault.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Clave Fernet: genérala UNA sola vez con CryptoService.generate_key()
    # y guárdala en variable de entorno FERNET_KEY
    app.config["FERNET_KEY"] = os.environ.get(
        "FERNET_KEY",
        "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="   # clave de ejemplo, CAMBIA EN PROD
    )

    # ── Inicializar extensiones ───────────────────────────────────────────────
    db.init_app(app)
    init_login_manager(app)

    # ── Registrar Blueprints (equivalente a @Controller mappings) ────────────
    app.register_blueprint(auth)
    app.register_blueprint(secret)

    # ── Crear tablas al arrancar ──────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5000)
