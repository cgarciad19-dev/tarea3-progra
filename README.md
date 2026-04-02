# TokenVault — Sistema de cifrado de texto con tokens

## Requisitos previos
- Python 3.11 o superior → https://python.org/downloads

## Instalación

```bash
# 1. Clona o descarga el proyecto
cd tokenvault

# 2. (Opcional pero recomendado) crea un entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta la aplicación
python app.py
```

## Acceder a la app
Abre tu navegador en: http://localhost:5000

## Variables de entorno (producción)
| Variable      | Descripción                                      |
|---------------|--------------------------------------------------|
| SECRET_KEY    | Clave secreta de Flask para sesiones             |
| FERNET_KEY    | Clave Fernet de 32 bytes en base64 urlsafe       |
| DATABASE_URL  | URL de SQLAlchemy (por defecto: sqlite local)    |

Para generar una FERNET_KEY nueva:
```python
from crypto_service import CryptoService
print(CryptoService.generate_key())
```

## Estructura del proyecto
```
tokenvault/
├── app.py              # Entrada y configuración (SecurityConfig)
├── models.py           # Entidades: User, SecretMessage, ViewAttempt
├── crypto_service.py   # CryptoService + EncryptionResult
├── user_service.py     # UserService + Flask-Login loader
├── auth_routes.py      # AuthController: /register, /login, /logout
├── secret_routes.py    # SecretController: /, /encrypt, /decrypt
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── home.html
└── static/
    └── css/style.css
```
