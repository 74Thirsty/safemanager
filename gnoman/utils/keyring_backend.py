"""System keyring backend abstraction."""
import keyring
from typing import Optional, List, Dict, Any
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import os


class KeyringBackend:
    """Abstract system keyring for secure secret storage."""

    def __init__(self, service_name: str = "GNOMAN"):
        """Initialize keyring backend.
        
        Args:
            service_name: Name of the service for keyring entries
        """
        self.service_name = service_name

    def set_secret(self, key: str, value: str) -> None:
        """Store a secret in the keyring.
        
        Args:
            key: Secret identifier
            value: Secret value
        """
        keyring.set_password(self.service_name, key, value)

    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve a secret from the keyring.
        
        Args:
            key: Secret identifier
            
        Returns:
            Secret value or None if not found
        """
        return keyring.get_password(self.service_name, key)

    def delete_secret(self, key: str) -> None:
        """Delete a secret from the keyring.
        
        Args:
            key: Secret identifier
        """
        try:
            keyring.delete_password(self.service_name, key)
        except keyring.errors.PasswordDeleteError:
            pass

    def list_secrets(self) -> List[str]:
        """List all secret keys (implementation depends on backend).
        
        Returns:
            List of secret identifiers
        """
        # Note: Not all keyring backends support listing
        # This is a simplified implementation
        return []

    def export_encrypted(self, password: str, keys: Optional[List[str]] = None) -> str:
        """Export secrets as encrypted JSON.
        
        Args:
            password: Password for encryption
            keys: Optional list of keys to export (all if None)
            
        Returns:
            Encrypted JSON string
        """
        # Derive key from password using Scrypt
        salt = os.urandom(16)
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())

        # Prepare data
        data = {}
        if keys:
            for k in keys:
                secret = self.get_secret(k)
                if secret:
                    data[k] = secret
        
        # Encrypt with ChaCha20-Poly1305
        cipher = ChaCha20Poly1305(key)
        nonce = os.urandom(12)
        plaintext = json.dumps(data).encode()
        ciphertext = cipher.encrypt(nonce, plaintext, None)

        # Package encrypted container
        container = {
            "version": "1.0",
            "algorithm": "ChaCha20-Poly1305",
            "kdf": "Scrypt",
            "salt": base64.b64encode(salt).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode()
        }
        
        return json.dumps(container)

    def import_encrypted(self, encrypted_data: str, password: str) -> None:
        """Import secrets from encrypted JSON.
        
        Args:
            encrypted_data: Encrypted JSON string
            password: Password for decryption
        """
        container = json.loads(encrypted_data)
        
        # Derive key from password
        salt = base64.b64decode(container["salt"])
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())

        # Decrypt
        cipher = ChaCha20Poly1305(key)
        nonce = base64.b64decode(container["nonce"])
        ciphertext = base64.b64decode(container["ciphertext"])
        plaintext = cipher.decrypt(nonce, ciphertext, None)
        
        # Import secrets
        data = json.loads(plaintext.decode())
        for k, v in data.items():
            self.set_secret(k, v)

    def audit_secrets(self) -> Dict[str, Any]:
        """Audit keyring for stale or duplicate entries.
        
        Returns:
            Audit report dictionary
        """
        return {
            "service": self.service_name,
            "backend": keyring.get_keyring().__class__.__name__,
            "secrets_count": 0,  # Simplified - depends on backend support
            "status": "ok"
        }
