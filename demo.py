#!/usr/bin/env python3
"""Demo script to showcase GNOMAN features"""
from gnoman.models.config import AppConfig
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.utils.keyring_manager import KeyringManager
from gnoman.models.data_models import WalletModel, SafeModel, ContractModel, AuditModel
from datetime import datetime

def main():
    print("=" * 60)
    print("GNOMAN Mission-Control Console - Feature Demo")
    print("=" * 60)
    print()
    
    # Initialize components
    print("1. Loading configuration...")
    config = AppConfig.load()
    print(f"   ✓ Data directory: {config.data_dir}")
    print(f"   ✓ Default chain: {config.default_chain_id}")
    print(f"   ✓ Chains configured: {len(config.chains)}")
    for chain_id, chain in config.chains.items():
        print(f"     - {chain.name} (ID: {chain_id})")
    print()
    
    # Initialize storage
    print("2. Initializing data storage...")
    storage = DataStore(config.data_dir)
    print(f"   ✓ Storage initialized at {config.data_dir}")
    print()
    
    # Initialize Web3 manager
    print("3. Setting up Web3 connections...")
    web3_manager = Web3Manager(config)
    print("   ✓ Web3Manager ready")
    print()
    
    # Initialize keyring
    print("4. Initializing secure keyring...")
    keyring_manager = KeyringManager(config.keyring_service)
    print("   ✓ Keyring ready for secure credential storage")
    print()
    
    # Create sample wallet
    print("5. Creating sample wallet...")
    account = web3_manager.create_account()
    wallet = WalletModel(
        name="demo-wallet",
        address=account["address"],
        chain_id=1,
        notes="Demo wallet created for testing"
    )
    storage.save_wallet(wallet)
    print(f"   ✓ Wallet created: {wallet.name}")
    print(f"   ✓ Address: {wallet.address}")
    print()
    
    # Create sample Safe
    print("6. Creating sample Safe multisig...")
    safe = SafeModel(
        name="demo-safe",
        address="0x1234567890123456789012345678901234567890",
        chain_id=1,
        threshold=2,
        owners=["0x" + "1" * 40, "0x" + "2" * 40, "0x" + "3" * 40],
        notes="Demo Safe with 2/3 multisig"
    )
    storage.save_safe(safe)
    print(f"   ✓ Safe created: {safe.name}")
    print(f"   ✓ Address: {safe.address}")
    print(f"   ✓ Threshold: {safe.threshold}/{len(safe.owners)}")
    print()
    
    # Create sample contract
    print("7. Creating sample contract...")
    contract = ContractModel(
        name="demo-contract",
        address="0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        chain_id=1,
        verified=True,
        notes="Demo smart contract"
    )
    storage.save_contract(contract)
    print(f"   ✓ Contract created: {contract.name}")
    print(f"   ✓ Address: {contract.address}")
    print()
    
    # Create audit log entry
    print("8. Logging audit event...")
    audit = AuditModel(
        event_type="demo_event",
        target="system",
        details={"action": "demo_initialization", "status": "success"},
        severity="info",
        user="demo_user"
    )
    storage.log_audit(audit)
    print(f"   ✓ Audit log entry created")
    print()
    
    # List all data
    print("9. Data summary:")
    print(f"   - Wallets: {len(storage.list_wallets())}")
    print(f"   - Safes: {len(storage.list_safes())}")
    print(f"   - Contracts: {len(storage.list_contracts())}")
    print(f"   - Audit entries: {len(storage.list_audits())}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("Run 'gnoman' to start the interactive console")
    print("=" * 60)

if __name__ == "__main__":
    main()
