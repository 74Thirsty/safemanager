"""Main entry point for GNOMAN."""
import click
import sys
from pathlib import Path
from gnoman.ui.app import GnomanApp
from gnoman.core.wallet_manager import WalletManager
from gnoman.core.safe_manager import SafeManager
from gnoman.core.audit_manager import AuditManager
from gnoman.utils.keyring_backend import KeyringBackend
from gnoman.utils.env_tools import EnvTools
from web3 import Web3


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """GNOMAN - Mission Control Console for Blockchain Ecosystem.
    
    A local, secure, and fully interactive dashboard for managing
    wallets, Gnosis Safes, and smart contracts.
    """
    pass


@cli.command()
@click.option('--rpc-url', default=None, help='Ethereum RPC URL')
@click.option('--headless', is_flag=True, help='Run in headless mode')
def run(rpc_url, headless):
    """Run the GNOMAN dashboard."""
    env_tools = EnvTools()
    
    if not rpc_url:
        rpc_url = env_tools.get_rpc_url()
    
    if headless:
        click.echo("Headless mode not yet fully implemented")
        click.echo(f"RPC URL: {rpc_url}")
        return
    
    # Run the Textual app
    app = GnomanApp(rpc_url=rpc_url)
    app.run()


@cli.group()
def wallet():
    """Wallet management commands."""
    pass


@wallet.command('generate')
@click.option('--name', required=True, help='Wallet name')
@click.option('--vanity', default=None, help='Vanity address prefix (hex)')
def wallet_generate(name, vanity):
    """Generate a new wallet."""
    keyring = KeyringBackend()
    wallet_manager = WalletManager(keyring)
    
    click.echo(f"Generating wallet: {name}")
    if vanity:
        click.echo(f"Finding vanity address with prefix: {vanity}")
    
    wallet = wallet_manager.generate_wallet(name, vanity)
    
    click.echo(f"\n✓ Wallet created successfully!")
    click.echo(f"  Name: {wallet['name']}")
    click.echo(f"  Address: {wallet['address']}")
    click.echo(f"\nPrivate key stored securely in system keyring.")


@wallet.command('list')
def wallet_list():
    """List all wallets."""
    keyring = KeyringBackend()
    wallet_manager = WalletManager(keyring)
    
    wallets = wallet_manager.list_wallets()
    
    if not wallets:
        click.echo("No wallets found.")
        return
    
    click.echo("\nWallets:")
    for w in wallets:
        click.echo(f"  • {w['name']}: {w['address']}")


@wallet.command('import')
@click.option('--name', required=True, help='Wallet name')
@click.option('--private-key', required=True, help='Private key (hex)')
def wallet_import(name, private_key):
    """Import a wallet from private key."""
    keyring = KeyringBackend()
    wallet_manager = WalletManager(keyring)
    
    wallet = wallet_manager.import_wallet(name, private_key)
    
    click.echo(f"\n✓ Wallet imported successfully!")
    click.echo(f"  Name: {wallet['name']}")
    click.echo(f"  Address: {wallet['address']}")


@cli.group()
def safe():
    """Safe management commands."""
    pass


@safe.command('list')
def safe_list():
    """List all Safes."""
    safe_manager = SafeManager()
    safes = safe_manager.list_safes()
    
    if not safes:
        click.echo("No Safes loaded.")
        return
    
    click.echo("\nSafes:")
    for s in safes:
        click.echo(f"  • {s['name']}: {s['address']}")


@safe.command('list-owners')
@click.option('--name', required=True, help='Safe name')
def safe_list_owners(name):
    """List Safe owners."""
    safe_manager = SafeManager()
    owners = safe_manager.get_owners(name)
    
    if not owners:
        click.echo(f"Safe '{name}' not found or has no owners.")
        return
    
    click.echo(f"\nOwners of {name}:")
    for owner in owners:
        click.echo(f"  • {owner}")


@cli.group()
def audit():
    """Audit log commands."""
    pass


@audit.command('run')
def audit_run():
    """Run audit verification."""
    audit_manager = AuditManager()
    result = audit_manager.verify_chain()
    
    click.echo(f"\n📝 Audit Verification")
    click.echo(f"  Status: {result['status']}")
    click.echo(f"  {result['message']}")


@audit.command('summary')
def audit_summary():
    """Show audit summary."""
    audit_manager = AuditManager()
    summary = audit_manager.get_summary()
    
    click.echo(f"\n📊 Audit Summary")
    click.echo(f"  Total Entries: {summary['total_entries']}")
    click.echo(f"  Status: {summary['verification_status']}")
    click.echo(f"  Last Action: {summary.get('last_action', 'None')}")


@audit.command('tail')
@click.option('--lines', default=10, help='Number of lines to show')
def audit_tail(lines):
    """Show recent audit logs."""
    audit_manager = AuditManager()
    logs = audit_manager.get_recent_logs(lines)
    
    if not logs:
        click.echo("No audit logs found.")
        return
    
    click.echo(f"\n📋 Recent Audit Logs ({lines} entries):")
    for log in logs:
        click.echo(f"  [{log['timestamp'][:19]}] {log['action_type']} - {log['user']}")


@cli.command()
def info():
    """Show GNOMAN system information."""
    env_tools = EnvTools()
    keyring = KeyringBackend()
    
    click.echo("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   GNOMAN — Mission Control v2.0                  ┃
┃   Local Gnosis Safe Manager & Keyring Vault      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)
    
    click.echo(f"RPC URL: {env_tools.get_rpc_url()}")
    click.echo(f"Network: {env_tools.get('network_name', 'Unknown')}")
    click.echo(f"Chain ID: {env_tools.get_chain_id()}")
    click.echo(f"Keyring Backend: {keyring.audit_secrets()['backend']}")
    click.echo(f"Config Dir: {env_tools.config_dir}")


if __name__ == "__main__":
    cli()
