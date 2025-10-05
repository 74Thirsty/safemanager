"""Wallet manager for GNOMAN."""
from typing import Optional, Dict, Any, List
from eth_account import Account
from web3 import Web3
from gnoman.utils.keyring_backend import KeyringBackend
import secrets


class WalletManager:
    """Manager for wallet operations."""

    def __init__(self, keyring: KeyringBackend, w3: Optional[Web3] = None):
        """Initialize wallet manager.
        
        Args:
            keyring: Keyring backend for secret storage
            w3: Web3 instance (optional)
        """
        self.keyring = keyring
        self.w3 = w3
        self.wallets: Dict[str, Dict[str, Any]] = {}

    def generate_wallet(self, name: str, vanity_prefix: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new wallet.
        
        Args:
            name: Wallet name
            vanity_prefix: Optional vanity address prefix (hex)
            
        Returns:
            Wallet info dictionary
        """
        if vanity_prefix:
            account = self._generate_vanity(vanity_prefix)
        else:
            account = Account.create()
        
        # Store private key in keyring
        self.keyring.set_secret(f"wallet_{name}_private_key", account.key.hex())
        
        wallet_info = {
            "name": name,
            "address": account.address,
            "balance": self._get_balance(account.address) if self.w3 else "0",
            "chain_id": self.w3.eth.chain_id if self.w3 else None
        }
        
        self.wallets[name] = wallet_info
        return wallet_info

    def _generate_vanity(self, prefix: str) -> Account:
        """Generate vanity address with prefix.
        
        Args:
            prefix: Hex prefix (without 0x)
            
        Returns:
            Account with matching address
        """
        prefix = prefix.lower()
        while True:
            account = Account.create()
            if account.address[2:].lower().startswith(prefix):
                return account

    def import_wallet(self, name: str, private_key: str) -> Dict[str, Any]:
        """Import wallet from private key.
        
        Args:
            name: Wallet name
            private_key: Private key hex string
            
        Returns:
            Wallet info dictionary
        """
        # Normalize private key
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        
        account = Account.from_key(private_key)
        
        # Store in keyring
        self.keyring.set_secret(f"wallet_{name}_private_key", private_key)
        
        wallet_info = {
            "name": name,
            "address": account.address,
            "balance": self._get_balance(account.address) if self.w3 else "0",
            "chain_id": self.w3.eth.chain_id if self.w3 else None
        }
        
        self.wallets[name] = wallet_info
        return wallet_info

    def get_wallet(self, name: str) -> Optional[Dict[str, Any]]:
        """Get wallet info by name.
        
        Args:
            name: Wallet name
            
        Returns:
            Wallet info or None
        """
        return self.wallets.get(name)

    def list_wallets(self) -> List[Dict[str, Any]]:
        """List all wallets.
        
        Returns:
            List of wallet info dictionaries
        """
        return list(self.wallets.values())

    def delete_wallet(self, name: str) -> None:
        """Delete wallet.
        
        Args:
            name: Wallet name
        """
        self.keyring.delete_secret(f"wallet_{name}_private_key")
        if name in self.wallets:
            del self.wallets[name]

    def export_wallet(self, name: str, password: str) -> str:
        """Export wallet as encrypted JSON.
        
        Args:
            name: Wallet name
            password: Encryption password
            
        Returns:
            Encrypted JSON string
        """
        return self.keyring.export_encrypted(password, [f"wallet_{name}_private_key"])

    def _get_balance(self, address: str) -> str:
        """Get wallet balance.
        
        Args:
            address: Wallet address
            
        Returns:
            Balance in ETH as string
        """
        if not self.w3:
            return "0"
        
        balance_wei = self.w3.eth.get_balance(address)
        return str(self.w3.from_wei(balance_wei, 'ether'))

    def update_balances(self) -> None:
        """Update all wallet balances."""
        if not self.w3:
            return
        
        for name, wallet in self.wallets.items():
            wallet["balance"] = self._get_balance(wallet["address"])

    def get_private_key(self, name: str) -> Optional[str]:
        """Get wallet private key from keyring.
        
        Args:
            name: Wallet name
            
        Returns:
            Private key hex string or None
        """
        return self.keyring.get_secret(f"wallet_{name}_private_key")

    def sign_message(self, name: str, message: str) -> Optional[str]:
        """Sign a message with wallet.
        
        Args:
            name: Wallet name
            message: Message to sign
            
        Returns:
            Signature hex string or None
        """
        private_key = self.get_private_key(name)
        if not private_key:
            return None
        
        account = Account.from_key(private_key)
        signed_message = account.sign_message(message.encode())
        return signed_message.signature.hex()
