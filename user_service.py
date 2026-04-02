from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from models import db, User


# ─── Equivalente a UserService ────────────────────────────────────────────────
class UserService:

    # ── equivalente a register(RegisterForm form): void ──────────────────────
    @staticmethod
    def register(username: str, email: str, password: str) -> User:
        if User.query.filter_by(username=username).first():
            raise ValueError("El nombre de usuario ya está en uso.")
        if User.query.filter_by(email=email).first():
            raise ValueError("El correo electrónico ya está registrado.")

        hashed = generate_password_hash(password)
        user   = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    # ── equivalente a findByUsername(String username): User ──────────────────
    @staticmethod
    def find_by_username(username: str) -> User | None:
        return User.query.filter_by(username=username).first()

    # ── equivalente a verifyPassword ─────────────────────────────────────────
    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        return check_password_hash(user.password, password)


# ─── Equivalente a CustomUserDetailsService (Flask-Login loader) ──────────────
def init_login_manager(app) -> LoginManager:
    login_manager = LoginManager(app)
    login_manager.login_view     = "auth.login"
    login_manager.login_message  = "Debes iniciar sesión para continuar."

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return db.session.get(User, int(user_id))

    return login_manager
