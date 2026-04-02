import uuid
from dataclasses import dataclass
from cryptography.fernet import Fernet


# ─── Equivalente a EncryptionResult (record/DTO) ──────────────────────────────
@dataclass
class EncryptionResult:
    encrypted_text: str
    token: str


# ─── Equivalente a CryptoService ──────────────────────────────────────────────
class CryptoService:
    """
    Servicio de cifrado/descifrado usando Fernet (AES-128-CBC + HMAC-SHA256).
    La clave se genera una vez y se guarda en la configuración de la app.
    """

    def __init__(self, secret_key: str):
        # La clave Fernet debe ser un bytes urlsafe-base64 de 32 bytes.
        # Se recibe como string desde la config y se convierte.
        self._fernet = Fernet(secret_key.encode())

    # ── equivalente a encrypt(String plainText): EncryptionResult ────────────
    def encrypt(self, plain_text: str) -> EncryptionResult:
        encrypted_bytes = self._fernet.encrypt(plain_text.encode("utf-8"))
        encrypted_text  = encrypted_bytes.decode("utf-8")
        token           = str(uuid.uuid4())
        return EncryptionResult(encrypted_text=encrypted_text, token=token)

    # ── equivalente a decrypt(String encryptedText, String iv): String ───────
    def decrypt(self, encrypted_text: str) -> str:
        decrypted_bytes = self._fernet.decrypt(encrypted_text.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")

    # ── utilidad para generar clave nueva (úsala una sola vez en setup) ───────
    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode("utf-8")
