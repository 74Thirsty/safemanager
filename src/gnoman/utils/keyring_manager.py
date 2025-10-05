"""Keyring utilities for secure credential storage"""
import keyring
from typing import Optional
from cryptography.fernet import Fernet
import base64
import hashlib


class KeyringManager:
    """Manages secure storage of credentials using system keyring"""
    
    def __init__(self, service_name: str = "gnoman"):
        self.service_name = service_name
    
    def store_secret(self, key: str, value: str) -> bool:
        """Store a secret in the keyring"""
        try:
            keyring.set_password(self.service_name, key, value)
            return True
        except Exception as e:
            print(f"Error storing secret: {e}")
            return False
    
    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve a secret from the keyring"""
        try:
            return keyring.get_password(self.service_name, key)
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return None
    
    def delete_secret(self, key: str) -> bool:
        """Delete a secret from the keyring"""
        try:
            keyring.delete_password(self.service_name, key)
            return True
        except Exception:
            return False
    
    def store_private_key(self, name: str, private_key: str, passphrase: str) -> bool:
        """Store an encrypted private key"""
        # Generate key from passphrase
        key = self._derive_key(passphrase)
        fernet = Fernet(key)
        
        # Encrypt the private key
        encrypted = fernet.encrypt(private_key.encode())
        
        # Store encrypted key
        return self.store_secret(f"pk_{name}", encrypted.decode())
    
    def get_private_key(self, name: str, passphrase: str) -> Optional[str]:
        """Retrieve and decrypt a private key"""
        encrypted = self.get_secret(f"pk_{name}")
        if not encrypted:
            return None
        
        try:
            key = self._derive_key(passphrase)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Error decrypting private key: {e}")
            return None
    
    @staticmethod
    def _derive_key(passphrase: str) -> bytes:
        """Derive encryption key from passphrase"""
        # Use PBKDF2-like approach with SHA256
        key = hashlib.sha256(passphrase.encode()).digest()
        return base64.urlsafe_b64encode(key)
