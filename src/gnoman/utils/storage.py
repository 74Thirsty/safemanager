"""Data storage management"""
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from gnoman.models.data_models import (
    WalletModel, SafeModel, ContractModel, 
    AuditModel, SecretModel
)


class DataStore:
    """Manages persistent storage of application data"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.wallets_dir = data_dir / "wallets"
        self.safes_dir = data_dir / "safes"
        self.contracts_dir = data_dir / "contracts"
        self.audits_dir = data_dir / "audits"
        
        for dir_path in [self.wallets_dir, self.safes_dir, self.contracts_dir, self.audits_dir]:
            dir_path.mkdir(exist_ok=True)
    
    # Wallet operations
    def save_wallet(self, wallet: WalletModel) -> bool:
        """Save wallet to disk"""
        try:
            file_path = self.wallets_dir / f"{wallet.name}.json"
            with open(file_path, "w") as f:
                json.dump(wallet.model_dump(mode='json'), f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving wallet: {e}")
            return False
    
    def load_wallet(self, name: str) -> Optional[WalletModel]:
        """Load wallet from disk"""
        try:
            file_path = self.wallets_dir / f"{name}.json"
            if not file_path.exists():
                return None
            
            with open(file_path, "r") as f:
                data = json.load(f)
            return WalletModel(**data)
        except Exception as e:
            print(f"Error loading wallet: {e}")
            return None
    
    def list_wallets(self) -> List[WalletModel]:
        """List all wallets"""
        wallets = []
        for file_path in self.wallets_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                wallets.append(WalletModel(**data))
            except Exception as e:
                print(f"Error loading wallet {file_path}: {e}")
        return wallets
    
    def delete_wallet(self, name: str) -> bool:
        """Delete wallet from disk"""
        try:
            file_path = self.wallets_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting wallet: {e}")
            return False
    
    # Safe operations
    def save_safe(self, safe: SafeModel) -> bool:
        """Save Safe to disk"""
        try:
            file_path = self.safes_dir / f"{safe.name}.json"
            with open(file_path, "w") as f:
                json.dump(safe.model_dump(mode='json'), f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving Safe: {e}")
            return False
    
    def load_safe(self, name: str) -> Optional[SafeModel]:
        """Load Safe from disk"""
        try:
            file_path = self.safes_dir / f"{name}.json"
            if not file_path.exists():
                return None
            
            with open(file_path, "r") as f:
                data = json.load(f)
            return SafeModel(**data)
        except Exception as e:
            print(f"Error loading Safe: {e}")
            return None
    
    def list_safes(self) -> List[SafeModel]:
        """List all Safes"""
        safes = []
        for file_path in self.safes_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                safes.append(SafeModel(**data))
            except Exception as e:
                print(f"Error loading Safe {file_path}: {e}")
        return safes
    
    def delete_safe(self, name: str) -> bool:
        """Delete Safe from disk"""
        try:
            file_path = self.safes_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting Safe: {e}")
            return False
    
    # Contract operations
    def save_contract(self, contract: ContractModel) -> bool:
        """Save contract to disk"""
        try:
            file_path = self.contracts_dir / f"{contract.name}.json"
            with open(file_path, "w") as f:
                json.dump(contract.model_dump(mode='json'), f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving contract: {e}")
            return False
    
    def load_contract(self, name: str) -> Optional[ContractModel]:
        """Load contract from disk"""
        try:
            file_path = self.contracts_dir / f"{name}.json"
            if not file_path.exists():
                return None
            
            with open(file_path, "r") as f:
                data = json.load(f)
            return ContractModel(**data)
        except Exception as e:
            print(f"Error loading contract: {e}")
            return None
    
    def list_contracts(self) -> List[ContractModel]:
        """List all contracts"""
        contracts = []
        for file_path in self.contracts_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                contracts.append(ContractModel(**data))
            except Exception as e:
                print(f"Error loading contract {file_path}: {e}")
        return contracts
    
    def delete_contract(self, name: str) -> bool:
        """Delete contract from disk"""
        try:
            file_path = self.contracts_dir / f"{name}.json"
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting contract: {e}")
            return False
    
    # Audit operations
    def log_audit(self, audit: AuditModel) -> bool:
        """Log an audit entry"""
        try:
            # Store audits by date
            date_str = audit.timestamp.strftime("%Y-%m-%d")
            file_path = self.audits_dir / f"{date_str}.jsonl"
            
            with open(file_path, "a") as f:
                f.write(json.dumps(audit.model_dump(mode='json'), default=str) + "\n")
            return True
        except Exception as e:
            print(f"Error logging audit: {e}")
            return False
    
    def list_audits(self, days: int = 7) -> List[AuditModel]:
        """List recent audit entries"""
        audits = []
        for file_path in sorted(self.audits_dir.glob("*.jsonl"), reverse=True)[:days]:
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        data = json.loads(line)
                        audits.append(AuditModel(**data))
            except Exception as e:
                print(f"Error loading audits {file_path}: {e}")
        return audits
