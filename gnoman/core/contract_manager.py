"""Contract manager for GNOMAN."""
from typing import Optional, Dict, Any, List
from web3 import Web3
from gnoman.utils.abi_tools import ABITools


class ContractManager:
    """Manager for smart contract interactions."""

    def __init__(self, w3: Optional[Web3] = None, abi_tools: Optional[ABITools] = None):
        """Initialize contract manager.
        
        Args:
            w3: Web3 instance
            abi_tools: ABI tools instance
        """
        self.w3 = w3
        self.abi_tools = abi_tools or ABITools()
        self.contracts: Dict[str, Dict[str, Any]] = {}

    def load_contract(
        self,
        name: str,
        address: str,
        abi: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Load a contract.
        
        Args:
            name: Contract name
            address: Contract address
            abi: Contract ABI
            
        Returns:
            Contract info dictionary
        """
        if not self.w3:
            raise ValueError("Web3 instance required")
        
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(address),
            abi=abi
        )
        
        contract_info = {
            "name": name,
            "address": address,
            "abi": abi,
            "contract": contract
        }
        
        self.contracts[name] = contract_info
        return contract_info

    def call_function(
        self,
        contract_name: str,
        function_name: str,
        args: List[Any] = None
    ) -> Any:
        """Call a contract function (read-only).
        
        Args:
            contract_name: Contract name
            function_name: Function to call
            args: Function arguments
            
        Returns:
            Function result
        """
        contract_info = self.contracts.get(contract_name)
        if not contract_info:
            raise ValueError(f"Contract {contract_name} not found")
        
        contract = contract_info["contract"]
        function = getattr(contract.functions, function_name)
        
        if args:
            return function(*args).call()
        else:
            return function().call()

    def prepare_transaction(
        self,
        contract_name: str,
        function_name: str,
        args: List[Any] = None,
        from_address: Optional[str] = None,
        value: int = 0
    ) -> Dict[str, Any]:
        """Prepare a contract transaction.
        
        Args:
            contract_name: Contract name
            function_name: Function to call
            args: Function arguments
            from_address: Sender address
            value: ETH value to send
            
        Returns:
            Transaction dictionary
        """
        contract_info = self.contracts.get(contract_name)
        if not contract_info:
            raise ValueError(f"Contract {contract_name} not found")
        
        contract = contract_info["contract"]
        function = getattr(contract.functions, function_name)
        
        # Build transaction
        if args:
            tx = function(*args).build_transaction({
                "from": from_address or "0x0000000000000000000000000000000000000000",
                "value": value,
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price if self.w3 else 0,
                "nonce": 0
            })
        else:
            tx = function().build_transaction({
                "from": from_address or "0x0000000000000000000000000000000000000000",
                "value": value,
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price if self.w3 else 0,
                "nonce": 0
            })
        
        return tx

    def simulate_function(
        self,
        contract_name: str,
        function_name: str,
        args: List[Any] = None
    ) -> Dict[str, Any]:
        """Simulate a function call locally.
        
        Args:
            contract_name: Contract name
            function_name: Function to call
            args: Function arguments
            
        Returns:
            Simulation result
        """
        try:
            result = self.call_function(contract_name, function_name, args)
            return {
                "status": "success",
                "result": result,
                "error": None
            }
        except Exception as e:
            return {
                "status": "error",
                "result": None,
                "error": str(e)
            }

    def list_functions(self, contract_name: str) -> List[Dict[str, Any]]:
        """List contract functions.
        
        Args:
            contract_name: Contract name
            
        Returns:
            List of function signatures
        """
        contract_info = self.contracts.get(contract_name)
        if not contract_info:
            return []
        
        abi = contract_info["abi"]
        functions = [
            item for item in abi
            if item.get("type") == "function"
        ]
        
        return functions

    def get_contract(self, name: str) -> Optional[Dict[str, Any]]:
        """Get contract info by name.
        
        Args:
            name: Contract name
            
        Returns:
            Contract info or None
        """
        return self.contracts.get(name)

    def list_contracts(self) -> List[str]:
        """List all loaded contracts.
        
        Returns:
            List of contract names
        """
        return list(self.contracts.keys())
