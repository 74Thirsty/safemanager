"""Cryptographic utilities for GNOMAN."""
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import os
import base64
from typing import Tuple


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using Scrypt KDF.
    
    Args:
        password: Password string
        salt: Salt bytes
        
    Returns:
        Derived key bytes
    """
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(data: bytes, password: str) -> Tuple[bytes, bytes, bytes]:
    """Encrypt data with ChaCha20-Poly1305.
    
    Args:
        data: Data to encrypt
        password: Password for encryption
        
    Returns:
        Tuple of (salt, nonce, ciphertext)
    """
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    cipher = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, data, None)
    
    return salt, nonce, ciphertext


def decrypt_data(salt: bytes, nonce: bytes, ciphertext: bytes, password: str) -> bytes:
    """Decrypt data with ChaCha20-Poly1305.
    
    Args:
        salt: Salt used for key derivation
        nonce: Nonce used for encryption
        ciphertext: Encrypted data
        password: Password for decryption
        
    Returns:
        Decrypted data bytes
    """
    key = derive_key(password, salt)
    cipher = ChaCha20Poly1305(key)
    return cipher.decrypt(nonce, ciphertext, None)


def generate_random_hex(length: int = 32) -> str:
    """Generate random hex string.
    
    Args:
        length: Length of random bytes (hex will be 2x this)
        
    Returns:
        Random hex string
    """
    return os.urandom(length).hex()
