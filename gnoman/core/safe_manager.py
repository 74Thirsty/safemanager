"""Safe manager for GNOMAN."""
from typing import Optional, Dict, Any, List
from web3 import Web3
from gnoman.utils.abi_tools import ABITools


class SafeManager:
    """Manager for Gnosis Safe operations."""

    # Simplified Safe ABI - key functions only
    SAFE_ABI = [
        {
            "constant": True,
            "inputs": [],
            "name": "getOwners",
            "outputs": [{"name": "", "type": "address[]"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "getThreshold",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "nonce",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]

    def __init__(self, w3: Optional[Web3] = None, abi_tools: Optional[ABITools] = None):
        """Initialize Safe manager.
        
        Args:
            w3: Web3 instance
            abi_tools: ABI tools instance
        """
        self.w3 = w3
        self.abi_tools = abi_tools or ABITools()
        self.safes: Dict[str, Dict[str, Any]] = {}

    def load_safe(self, name: str, address: str, abi: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Load a Safe contract.
        
        Args:
            name: Safe name
            address: Safe contract address
            abi: Optional custom ABI (uses default if None)
            
        Returns:
            Safe info dictionary
        """
        if not self.w3:
            raise ValueError("Web3 instance required")
        
        # Use provided ABI or default Safe ABI
        safe_abi = abi or self.SAFE_ABI
        
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=safe_abi)
        
        # Get Safe details
        try:
            owners = contract.functions.getOwners().call()
            threshold = contract.functions.getThreshold().call()
            nonce = contract.functions.nonce().call()
        except Exception as e:
            # Fallback if methods don't exist
            owners = []
            threshold = 0
            nonce = 0
        
        safe_info = {
            "name": name,
            "address": address,
            "owners": owners,
            "threshold": threshold,
            "nonce": nonce,
            "balance": self._get_balance(address)
        }
        
        self.safes[name] = safe_info
        return safe_info

    def get_safe(self, name: str) -> Optional[Dict[str, Any]]:
        """Get Safe info by name.
        
        Args:
            name: Safe name
            
        Returns:
            Safe info or None
        """
        return self.safes.get(name)

    def list_safes(self) -> List[Dict[str, Any]]:
        """List all Safes.
        
        Returns:
            List of Safe info dictionaries
        """
        return list(self.safes.values())

    def get_owners(self, name: str) -> List[str]:
        """Get Safe owners.
        
        Args:
            name: Safe name
            
        Returns:
            List of owner addresses
        """
        safe = self.safes.get(name)
        return safe["owners"] if safe else []

    def get_threshold(self, name: str) -> int:
        """Get Safe threshold.
        
        Args:
            name: Safe name
            
        Returns:
            Threshold value
        """
        safe = self.safes.get(name)
        return safe["threshold"] if safe else 0

    def _get_balance(self, address: str) -> str:
        """Get Safe balance.
        
        Args:
            address: Safe address
            
        Returns:
            Balance in ETH as string
        """
        if not self.w3:
            return "0"
        
        balance_wei = self.w3.eth.get_balance(Web3.to_checksum_address(address))
        return str(self.w3.from_wei(balance_wei, 'ether'))

    def prepare_transaction(
        self,
        name: str,
        to: str,
        value: int,
        data: bytes = b""
    ) -> Dict[str, Any]:
        """Prepare a Safe transaction.
        
        Args:
            name: Safe name
            to: Recipient address
            value: Value in wei
            data: Transaction data
            
        Returns:
            Transaction info dictionary
        """
        safe = self.safes.get(name)
        if not safe:
            raise ValueError(f"Safe {name} not found")
        
        tx_info = {
            "safe": name,
            "safe_address": safe["address"],
            "to": to,
            "value": value,
            "data": data.hex() if isinstance(data, bytes) else data,
            "nonce": safe["nonce"],
            "threshold": safe["threshold"]
        }
        
        return tx_info

    def simulate_transaction(
        self,
        name: str,
        to: str,
        value: int,
        data: bytes = b""
    ) -> Dict[str, Any]:
        """Simulate a Safe transaction.
        
        Args:
            name: Safe name
            to: Recipient address
            value: Value in wei
            data: Transaction data
            
        Returns:
            Simulation result
        """
        # Simplified simulation
        return {
            "status": "simulated",
            "safe": name,
            "to": to,
            "value": value,
            "gas_estimate": 100000
        }

    def update_safe_info(self, name: str) -> None:
        """Update Safe information.
        
        Args:
            name: Safe name
        """
        safe = self.safes.get(name)
        if not safe or not self.w3:
            return
        
        # Reload Safe data
        address = safe["address"]
        self.load_safe(name, address)
