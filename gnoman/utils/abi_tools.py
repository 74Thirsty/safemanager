"""ABI tools for contract interaction."""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from web3 import Web3


class ABITools:
    """Tools for loading, parsing, and caching ABIs."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize ABI tools.
        
        Args:
            cache_dir: Directory for caching ABIs
        """
        self.cache_dir = cache_dir or Path.home() / ".gnoman" / "abi_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_abis: Dict[str, List[Dict[str, Any]]] = {}

    def load_abi(self, abi_path: str, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load ABI from file.
        
        Args:
            abi_path: Path to ABI JSON file
            name: Optional name for caching
            
        Returns:
            ABI list
        """
        with open(abi_path, 'r') as f:
            abi = json.load(f)
        
        if name:
            self.loaded_abis[name] = abi
            # Cache it
            cache_path = self.cache_dir / f"{name}.json"
            with open(cache_path, 'w') as f:
                json.dump(abi, f, indent=2)
        
        return abi

    def parse_abi_string(self, abi_str: str, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Parse ABI from JSON string.
        
        Args:
            abi_str: ABI as JSON string
            name: Optional name for caching
            
        Returns:
            ABI list
        """
        abi = json.loads(abi_str)
        
        if name:
            self.loaded_abis[name] = abi
        
        return abi

    def get_function_signature(self, abi: List[Dict[str, Any]], function_name: str) -> Optional[Dict[str, Any]]:
        """Get function signature from ABI.
        
        Args:
            abi: ABI list
            function_name: Name of the function
            
        Returns:
            Function signature dict or None
        """
        for item in abi:
            if item.get("type") == "function" and item.get("name") == function_name:
                return item
        return None

    def validate_inputs(
        self, 
        function_sig: Dict[str, Any], 
        inputs: List[Any]
    ) -> bool:
        """Validate function inputs against signature.
        
        Args:
            function_sig: Function signature from ABI
            inputs: Input values
            
        Returns:
            True if valid
        """
        expected_inputs = function_sig.get("inputs", [])
        if len(inputs) != len(expected_inputs):
            return False
        
        # Basic validation - could be extended
        return True

    def encode_function_call(
        self,
        w3: Web3,
        abi: List[Dict[str, Any]],
        function_name: str,
        args: List[Any]
    ) -> bytes:
        """Encode function call data.
        
        Args:
            w3: Web3 instance
            abi: Contract ABI
            function_name: Function to call
            args: Function arguments
            
        Returns:
            Encoded function call data
        """
        contract = w3.eth.contract(abi=abi)
        return contract.encodeABI(fn_name=function_name, args=args)

    def list_cached_abis(self) -> List[str]:
        """List cached ABI names.
        
        Returns:
            List of cached ABI names
        """
        return [f.stem for f in self.cache_dir.glob("*.json")]

    def get_cached_abi(self, name: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached ABI by name.
        
        Args:
            name: ABI name
            
        Returns:
            ABI list or None
        """
        cache_path = self.cache_dir / f"{name}.json"
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None
