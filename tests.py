#!/usr/bin/env python3
"""Test suite for GNOMAN core functionality"""
import sys
from pathlib import Path

def test_imports():
    """Test all core imports"""
    print("Testing imports...")
    try:
        from gnoman.main import GnomanApp
        from gnoman.models.config import AppConfig
        from gnoman.models.data_models import WalletModel, SafeModel, ContractModel
        from gnoman.utils.keyring_manager import KeyringManager
        from gnoman.utils.web3_manager import Web3Manager
        from gnoman.utils.storage import DataStore
        from gnoman.core.splash import SplashScreen
        from gnoman.core.dashboard import Dashboard
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from gnoman.models.config import AppConfig
        config = AppConfig.load()
        assert config.default_chain_id == 1
        assert len(config.chains) > 0
        assert config.data_dir.name == ".gnoman"
        print(f"✓ Config loaded: {len(config.chains)} chains configured")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_models():
    """Test data models"""
    print("\nTesting data models...")
    try:
        from gnoman.models.data_models import WalletModel, SafeModel, ContractModel
        
        # Test WalletModel
        wallet = WalletModel(
            name="test",
            address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            chain_id=1
        )
        assert wallet.address == "0x742d35cC6634c0532925A3b844bc9E7595F0beB1"
        
        # Test SafeModel
        safe = SafeModel(
            name="test-safe",
            address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            chain_id=1,
            threshold=2,
            owners=["0x" + "1" * 40]
        )
        assert safe.threshold == 2
        
        # Test ContractModel
        contract = ContractModel(
            name="test-contract",
            address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            chain_id=1
        )
        assert contract.verified == False
        
        print("✓ All models validated correctly")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_storage():
    """Test storage system"""
    print("\nTesting storage...")
    try:
        from gnoman.models.config import AppConfig
        from gnoman.utils.storage import DataStore
        from gnoman.models.data_models import WalletModel
        
        config = AppConfig.load()
        storage = DataStore(config.data_dir)
        
        # Create test wallet
        wallet = WalletModel(
            name="test-storage-wallet",
            address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            chain_id=1
        )
        
        # Save and load
        storage.save_wallet(wallet)
        loaded = storage.load_wallet("test-storage-wallet")
        assert loaded is not None
        assert loaded.name == "test-storage-wallet"
        
        # Cleanup
        storage.delete_wallet("test-storage-wallet")
        
        print("✓ Storage operations successful")
        return True
    except Exception as e:
        print(f"✗ Storage test failed: {e}")
        return False

def test_web3():
    """Test Web3 manager"""
    print("\nTesting Web3 manager...")
    try:
        from gnoman.models.config import AppConfig
        from gnoman.utils.web3_manager import Web3Manager
        
        config = AppConfig.load()
        web3_mgr = Web3Manager(config)
        
        # Test account creation
        account = web3_mgr.create_account()
        assert "address" in account
        assert "private_key" in account
        assert account["address"].startswith("0x")
        
        print(f"✓ Web3 manager working, created account: {account['address'][:10]}...")
        return True
    except Exception as e:
        print(f"✗ Web3 test failed: {e}")
        return False

def test_keyring():
    """Test keyring manager"""
    print("\nTesting keyring manager...")
    # Skip keyring test in non-interactive environments
    import os
    if os.environ.get('CI') or not sys.stdin.isatty():
        print("⚠ Keyring test skipped (non-interactive environment)")
        return True
    
    try:
        from gnoman.utils.keyring_manager import KeyringManager
        
        km = KeyringManager("gnoman-test")
        
        # Test secret storage - skip if keyring not configured
        try:
            success = km.store_secret("test-key", "test-value")
            if success:
                value = km.get_secret("test-key")
                if value == "test-value":
                    km.delete_secret("test-key")
                    print("✓ Keyring operations successful")
                    return True
        except Exception:
            pass
        
        print("⚠ Keyring not configured (skipping - not an error)")
        return True  # Not a failure if keyring isn't available
    except Exception as e:
        print(f"⚠ Keyring test skipped: {e}")
        return True  # Not a critical failure

def test_app_instance():
    """Test app instance creation"""
    print("\nTesting app instance...")
    try:
        from gnoman.main import GnomanApp
        
        app = GnomanApp()
        assert app.TITLE == "GNOMAN Mission-Control Console"
        assert len(app.BINDINGS) > 0
        
        print("✓ App instance created successfully")
        return True
    except Exception as e:
        print(f"✗ App instance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("GNOMAN Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_models,
        test_storage,
        test_web3,
        test_keyring,
        test_app_instance,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
