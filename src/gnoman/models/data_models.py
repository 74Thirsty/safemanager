"""Data models for GNOMAN application"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from eth_utils import is_address, to_checksum_address


class WalletModel(BaseModel):
    """Wallet data model"""
    name: str
    address: str
    chain_id: int = 1
    balance: str = "0"
    created_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        if not is_address(v):
            raise ValueError(f"Invalid Ethereum address: {v}")
        return to_checksum_address(v)


class SafeModel(BaseModel):
    """Gnosis Safe multisig data model"""
    name: str
    address: str
    chain_id: int = 1
    threshold: int = 1
    owners: List[str] = Field(default_factory=list)
    balance: str = "0"
    nonce: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        if not is_address(v):
            raise ValueError(f"Invalid Ethereum address: {v}")
        return to_checksum_address(v)
    
    @field_validator('owners')
    @classmethod
    def validate_owners(cls, v: List[str]) -> List[str]:
        return [to_checksum_address(addr) if is_address(addr) else addr for addr in v]


class ContractModel(BaseModel):
    """Smart contract data model"""
    name: str
    address: str
    chain_id: int = 1
    abi: List[Dict[str, Any]] = Field(default_factory=list)
    implementation: Optional[str] = None
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        if not is_address(v):
            raise ValueError(f"Invalid Ethereum address: {v}")
        return to_checksum_address(v)


class AuditModel(BaseModel):
    """Audit log entry model"""
    timestamp: datetime = Field(default_factory=datetime.now)
    event_type: str
    target: str
    details: Dict[str, Any] = Field(default_factory=dict)
    severity: str = "info"  # info, warning, error, critical
    user: Optional[str] = None


class SecretModel(BaseModel):
    """Secret data model"""
    name: str
    service: str
    username: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
