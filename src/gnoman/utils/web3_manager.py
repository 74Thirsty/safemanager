"""Web3 utilities for blockchain interaction"""
from typing import Optional, Dict, Any, List
from web3 import Web3
try:
    # For newer versions of web3.py (7.x+)
    from web3.middleware import ExtraDataToPOAMiddleware as geth_poa_middleware
except ImportError:
    # Fallback for older versions
    try:
        from web3.middleware import geth_poa_middleware
    except ImportError:
        geth_poa_middleware = None
from eth_account import Account
from gnoman.models.config import AppConfig, ChainConfig


class Web3Manager:
    """Manages Web3 connections and blockchain interactions"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.connections: Dict[int, Web3] = {}
    
    def get_web3(self, chain_id: int) -> Optional[Web3]:
        """Get or create Web3 connection for a chain"""
        if chain_id in self.connections:
            return self.connections[chain_id]
        
        chain_config = self.config.chains.get(chain_id)
        if not chain_config:
            return None
        
        try:
            w3 = Web3(Web3.HTTPProvider(chain_config.rpc_url))
            # Add PoA middleware for networks like Polygon
            if chain_id in [137, 80001] and geth_poa_middleware:  # Polygon networks
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            self.connections[chain_id] = w3
            return w3
        except Exception as e:
            print(f"Error connecting to chain {chain_id}: {e}")
            return None
    
    def get_balance(self, address: str, chain_id: int) -> Optional[str]:
        """Get balance for an address"""
        w3 = self.get_web3(chain_id)
        if not w3:
            return None
        
        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return str(balance_eth)
        except Exception as e:
            print(f"Error getting balance: {e}")
            return None
    
    def get_transaction_count(self, address: str, chain_id: int) -> Optional[int]:
        """Get transaction count (nonce) for an address"""
        w3 = self.get_web3(chain_id)
        if not w3:
            return None
        
        try:
            return w3.eth.get_transaction_count(address)
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return None
    
    def get_code(self, address: str, chain_id: int) -> Optional[str]:
        """Get contract code at address"""
        w3 = self.get_web3(chain_id)
        if not w3:
            return None
        
        try:
            code = w3.eth.get_code(address)
            return code.hex()
        except Exception as e:
            print(f"Error getting code: {e}")
            return None
    
    def is_contract(self, address: str, chain_id: int) -> bool:
        """Check if address is a contract"""
        code = self.get_code(address, chain_id)
        return code is not None and code != "0x"
    
    def create_account(self) -> Dict[str, str]:
        """Create a new Ethereum account"""
        account = Account.create()
        return {
            "address": account.address,
            "private_key": account.key.hex()
        }
    
    def sign_message(self, message: str, private_key: str) -> str:
        """Sign a message with a private key"""
        account = Account.from_key(private_key)
        signed = account.sign_message(message.encode())
        return signed.signature.hex()
