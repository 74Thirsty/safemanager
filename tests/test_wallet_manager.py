"""Tests for wallet manager."""
import pytest
from gnoman.core.wallet_manager import WalletManager
from gnoman.utils.keyring_backend import KeyringBackend
from unittest.mock import Mock


@pytest.fixture
def mock_keyring():
    """Create a mock keyring backend."""
    keyring = Mock(spec=KeyringBackend)
    keyring.secrets = {}
    
    def set_secret(key, value):
        keyring.secrets[key] = value
    
    def get_secret(key):
        return keyring.secrets.get(key)
    
    def delete_secret(key):
        keyring.secrets.pop(key, None)
    
    keyring.set_secret = set_secret
    keyring.get_secret = get_secret
    keyring.delete_secret = delete_secret
    
    return keyring


def test_generate_wallet(mock_keyring):
    """Test wallet generation."""
    wallet_manager = WalletManager(mock_keyring)
    
    wallet = wallet_manager.generate_wallet("test_wallet")
    
    assert wallet["name"] == "test_wallet"
    assert wallet["address"].startswith("0x")
    assert len(wallet["address"]) == 42
    
    # Verify private key stored in keyring
    private_key = mock_keyring.get_secret("wallet_test_wallet_private_key")
    assert private_key is not None
    assert private_key.startswith("0x")


def test_import_wallet(mock_keyring):
    """Test wallet import."""
    wallet_manager = WalletManager(mock_keyring)
    
    # Known test private key (DO NOT USE IN PRODUCTION)
    test_private_key = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    wallet = wallet_manager.import_wallet("imported_wallet", test_private_key)
    
    assert wallet["name"] == "imported_wallet"
    assert wallet["address"].startswith("0x")
    
    # Verify private key stored
    stored_key = mock_keyring.get_secret("wallet_imported_wallet_private_key")
    assert stored_key == test_private_key


def test_list_wallets(mock_keyring):
    """Test listing wallets."""
    wallet_manager = WalletManager(mock_keyring)
    
    wallet_manager.generate_wallet("wallet1")
    wallet_manager.generate_wallet("wallet2")
    
    wallets = wallet_manager.list_wallets()
    
    assert len(wallets) == 2
    assert any(w["name"] == "wallet1" for w in wallets)
    assert any(w["name"] == "wallet2" for w in wallets)


def test_delete_wallet(mock_keyring):
    """Test wallet deletion."""
    wallet_manager = WalletManager(mock_keyring)
    
    wallet_manager.generate_wallet("to_delete")
    assert len(wallet_manager.list_wallets()) == 1
    
    wallet_manager.delete_wallet("to_delete")
    assert len(wallet_manager.list_wallets()) == 0
    
    # Verify keyring entry deleted
    assert mock_keyring.get_secret("wallet_to_delete_private_key") is None


def test_get_wallet(mock_keyring):
    """Test getting wallet by name."""
    wallet_manager = WalletManager(mock_keyring)
    
    created = wallet_manager.generate_wallet("test")
    retrieved = wallet_manager.get_wallet("test")
    
    assert retrieved is not None
    assert retrieved["name"] == created["name"]
    assert retrieved["address"] == created["address"]


def test_get_nonexistent_wallet(mock_keyring):
    """Test getting nonexistent wallet."""
    wallet_manager = WalletManager(mock_keyring)
    
    wallet = wallet_manager.get_wallet("nonexistent")
    assert wallet is None
