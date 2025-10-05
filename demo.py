#!/usr/bin/env python3
"""
GNOMAN Demo - Shows basic usage without full installation.

This demo shows how to use GNOMAN's core functionality programmatically.
"""

import sys
from pathlib import Path

# Add gnoman to path for demo purposes
sys.path.insert(0, str(Path(__file__).parent))

from gnoman.core.wallet_manager import WalletManager
from gnoman.core.audit_manager import AuditManager
from gnoman.utils.keyring_backend import KeyringBackend


class MockKeyring:
    """Mock keyring for demo (doesn't actually store in system keyring)."""
    
    def __init__(self):
        self.secrets = {}
    
    def set_secret(self, key, value):
        self.secrets[key] = value
        print(f"  [Keyring] Stored secret: {key}")
    
    def get_secret(self, key):
        return self.secrets.get(key)
    
    def delete_secret(self, key):
        self.secrets.pop(key, None)
        print(f"  [Keyring] Deleted secret: {key}")
    
    def export_encrypted(self, password, keys=None):
        return "{encrypted_data}"
    
    def audit_secrets(self):
        return {"backend": "MockKeyring", "secrets_count": len(self.secrets), "status": "ok"}


def demo_wallet_operations():
    """Demonstrate wallet operations."""
    print("\n" + "="*60)
    print("GNOMAN DEMO - Wallet Operations")
    print("="*60)
    
    keyring = MockKeyring()
    wallet_manager = WalletManager(keyring)
    
    print("\n1. Generating a new wallet...")
    wallet1 = wallet_manager.generate_wallet("demo_wallet")
    print(f"   ✓ Created wallet: {wallet1['name']}")
    print(f"   ✓ Address: {wallet1['address']}")
    
    print("\n2. Generating wallet with vanity address (prefix '00')...")
    print("   (This may take a moment...)")
    wallet2 = wallet_manager.generate_wallet("vanity_wallet", vanity_prefix="00")
    print(f"   ✓ Created wallet: {wallet2['name']}")
    print(f"   ✓ Address: {wallet2['address']}")
    
    print("\n3. Listing all wallets...")
    wallets = wallet_manager.list_wallets()
    for w in wallets:
        print(f"   • {w['name']}: {w['address']}")
    
    print("\n4. Getting wallet details...")
    wallet = wallet_manager.get_wallet("demo_wallet")
    print(f"   Name: {wallet['name']}")
    print(f"   Address: {wallet['address']}")
    print(f"   Balance: {wallet['balance']} ETH")
    
    print("\n5. Private key is stored securely in keyring...")
    private_key = wallet_manager.get_private_key("demo_wallet")
    print(f"   Private key (first 20 chars): {private_key[:20]}...")
    
    print("\n6. Deleting a wallet...")
    wallet_manager.delete_wallet("demo_wallet")
    remaining = wallet_manager.list_wallets()
    print(f"   Remaining wallets: {len(remaining)}")


def demo_audit_operations():
    """Demonstrate audit operations."""
    print("\n" + "="*60)
    print("GNOMAN DEMO - Audit Logging")
    print("="*60)
    
    audit = AuditManager()
    
    print("\n1. Logging actions...")
    audit.log_action("wallet_created", {"name": "demo_wallet"}, "demo_user")
    audit.log_action("wallet_imported", {"name": "imported"}, "demo_user")
    audit.log_action("safe_loaded", {"address": "0x123..."}, "demo_user")
    print("   ✓ Logged 3 actions")
    
    print("\n2. Verifying audit chain integrity...")
    result = audit.verify_chain()
    print(f"   Status: {result['status']}")
    print(f"   Entries: {result['entries']}")
    print(f"   Message: {result['message']}")
    
    print("\n3. Getting recent logs...")
    logs = audit.get_recent_logs(3)
    for log in logs:
        print(f"   [{log['timestamp'][:19]}] {log['action_type']} by {log['user']}")
    
    print("\n4. Getting audit summary...")
    summary = audit.get_summary()
    print(f"   Total entries: {summary['total_entries']}")
    print(f"   Verification: {summary['verification_status']}")
    print(f"   Last action: {summary.get('last_action')}")


def demo_system_info():
    """Show system information."""
    print("\n" + "="*60)
    print("GNOMAN DEMO - System Information")
    print("="*60)
    
    from gnoman.utils.env_tools import EnvTools
    
    env = EnvTools()
    
    print("\n📡 Configuration:")
    print(f"   RPC URL: {env.get_rpc_url()}")
    print(f"   Chain ID: {env.get_chain_id()}")
    print(f"   Network: {env.get('network_name', 'Unknown')}")
    print(f"   Config Dir: {env.config_dir}")
    
    keyring = MockKeyring()
    keyring_info = keyring.audit_secrets()
    
    print("\n🔐 Keyring:")
    print(f"   Backend: {keyring_info['backend']}")
    print(f"   Status: {keyring_info['status']}")


def main():
    """Run all demos."""
    print("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   GNOMAN — Mission Control v2.0                  ┃
┃   Local Gnosis Safe Manager & Keyring Vault      ┃
┃   DEMO MODE                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)
    
    demo_system_info()
    demo_wallet_operations()
    demo_audit_operations()
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)
    print("\nTo use the full TUI interface, install dependencies:")
    print("  pip install -e .")
    print("\nThen run:")
    print("  gnoman run")
    print()


if __name__ == "__main__":
    main()
