"""Environment and configuration utilities."""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import json


class EnvTools:
    """Environment and configuration management."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize environment tools.
        
        Args:
            config_dir: Directory for configuration files
        """
        self.config_dir = config_dir or Path.home() / ".gnoman"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()
            self.save_config()

    def _default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default config dictionary
        """
        return {
            "rpc_url": os.getenv("ETH_RPC_URL", "http://localhost:8545"),
            "chain_id": int(os.getenv("CHAIN_ID", "1")),
            "network_name": os.getenv("NETWORK_NAME", "mainnet"),
            "keyring_service": "GNOMAN",
            "audit_enabled": True,
            "last_session": None
        }

    def save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save_config()

    def load_env_file(self, env_path: Optional[str] = None) -> None:
        """Load environment variables from .env file.
        
        Args:
            env_path: Path to .env file
        """
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()

    def get_rpc_url(self) -> str:
        """Get RPC URL.
        
        Returns:
            RPC URL
        """
        return self.get("rpc_url", "http://localhost:8545")

    def get_chain_id(self) -> int:
        """Get chain ID.
        
        Returns:
            Chain ID
        """
        return self.get("chain_id", 1)

    def sync_with_env(self) -> None:
        """Sync configuration with environment variables."""
        if os.getenv("ETH_RPC_URL"):
            self.set("rpc_url", os.getenv("ETH_RPC_URL"))
        if os.getenv("CHAIN_ID"):
            self.set("chain_id", int(os.getenv("CHAIN_ID")))
        if os.getenv("NETWORK_NAME"):
            self.set("network_name", os.getenv("NETWORK_NAME"))
