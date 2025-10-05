"""Configuration models and management"""
import os
from typing import Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field
import yaml


class ChainConfig(BaseModel):
    """Blockchain network configuration"""
    chain_id: int
    name: str
    rpc_url: str
    explorer_url: str
    currency_symbol: str = "ETH"


class AppConfig(BaseModel):
    """Application configuration"""
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".gnoman")
    keyring_service: str = "gnoman"
    default_chain_id: int = 1
    chains: Dict[int, ChainConfig] = Field(default_factory=dict)
    theme: str = "dark"
    auto_save: bool = True
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "wallets").mkdir(exist_ok=True)
        (self.data_dir / "safes").mkdir(exist_ok=True)
        (self.data_dir / "contracts").mkdir(exist_ok=True)
        (self.data_dir / "audits").mkdir(exist_ok=True)
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "AppConfig":
        """Load configuration from file"""
        if config_path is None:
            config_path = Path.home() / ".gnoman" / "config.yaml"
        
        if config_path.exists():
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
                return cls(**data)
        
        # Return default config with common chains
        config = cls()
        config.chains = {
            1: ChainConfig(
                chain_id=1,
                name="Ethereum Mainnet",
                rpc_url="https://eth.llamarpc.com",
                explorer_url="https://etherscan.io",
                currency_symbol="ETH"
            ),
            5: ChainConfig(
                chain_id=5,
                name="Goerli Testnet",
                rpc_url="https://goerli.infura.io/v3/",
                explorer_url="https://goerli.etherscan.io",
                currency_symbol="ETH"
            ),
            11155111: ChainConfig(
                chain_id=11155111,
                name="Sepolia Testnet",
                rpc_url="https://sepolia.infura.io/v3/",
                explorer_url="https://sepolia.etherscan.io",
                currency_symbol="ETH"
            ),
            137: ChainConfig(
                chain_id=137,
                name="Polygon Mainnet",
                rpc_url="https://polygon-rpc.com",
                explorer_url="https://polygonscan.com",
                currency_symbol="MATIC"
            )
        }
        return config
    
    def save(self, config_path: Optional[Path] = None):
        """Save configuration to file"""
        if config_path is None:
            config_path = Path.home() / ".gnoman" / "config.yaml"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "w") as f:
            yaml.dump(self.model_dump(mode='json'), f, default_flow_style=False)
