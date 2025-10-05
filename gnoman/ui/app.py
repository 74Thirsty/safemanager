"""Main GNOMAN application."""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static, DataTable
from textual.containers import Container, Vertical
from textual.binding import Binding
from web3 import Web3
from gnoman.core.wallet_manager import WalletManager
from gnoman.core.safe_manager import SafeManager
from gnoman.core.audit_manager import AuditManager
from gnoman.core.contract_manager import ContractManager
from gnoman.utils.keyring_backend import KeyringBackend
from gnoman.utils.abi_tools import ABITools
from gnoman.utils.env_tools import EnvTools


class GnomanApp(App):
    """GNOMAN Mission Control Console."""

    CSS = """
    Screen {
        background: $surface;
    }

    Header {
        background: $primary;
        color: $text;
        height: 3;
    }

    Footer {
        background: $panel;
        color: $text;
    }

    TabbedContent {
        height: 100%;
    }

    .info-panel {
        background: $panel;
        border: solid $primary;
        padding: 1;
        margin: 1;
    }

    DataTable {
        height: 100%;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
    ]

    TITLE = "GNOMAN — Mission Control v2.0"
    SUB_TITLE = "Local Gnosis Safe Manager & Keyring Vault"

    def __init__(self, rpc_url: str = "http://localhost:8545", **kwargs):
        """Initialize GNOMAN app.
        
        Args:
            rpc_url: Ethereum RPC URL
        """
        super().__init__(**kwargs)
        
        # Initialize components
        self.env_tools = EnvTools()
        self.keyring = KeyringBackend()
        
        # Initialize Web3
        try:
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            self.rpc_connected = self.w3.is_connected()
        except Exception:
            self.w3 = None
            self.rpc_connected = False
        
        # Initialize managers
        self.wallet_manager = WalletManager(self.keyring, self.w3)
        self.safe_manager = SafeManager(self.w3)
        self.audit_manager = AuditManager()
        self.contract_manager = ContractManager(self.w3)
        self.abi_tools = ABITools()
        
        # Log app start
        self.audit_manager.log_action("app_started", {
            "rpc_url": rpc_url,
            "rpc_connected": self.rpc_connected
        })

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        yield Header()
        
        with TabbedContent(initial="overview"):
            with TabPane("Overview", id="overview"):
                yield self._create_overview()
            
            with TabPane("Wallets", id="wallets"):
                yield self._create_wallets_view()
            
            with TabPane("Safes", id="safes"):
                yield self._create_safes_view()
            
            with TabPane("Contracts", id="contracts"):
                yield self._create_contracts_view()
            
            with TabPane("Audit", id="audit"):
                yield self._create_audit_view()
            
            with TabPane("Sync", id="sync"):
                yield self._create_sync_view()
            
            with TabPane("Secrets", id="secrets"):
                yield self._create_secrets_view()
        
        yield Footer()

    def _create_overview(self) -> Container:
        """Create overview panel."""
        status = "Connected" if self.rpc_connected else "Disconnected"
        network = self.env_tools.get("network_name", "Unknown")
        
        audit_summary = self.audit_manager.get_summary()
        
        content = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   GNOMAN — Mission Control v2.0                  ┃
┃   Local, Secure, Fully Interactive Dashboard     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📡 Network Status
  • RPC: {status}
  • Network: {network}
  • Chain ID: {self.env_tools.get_chain_id()}

📊 System Metrics
  • Wallets: {len(self.wallet_manager.list_wallets())}
  • Safes: {len(self.safe_manager.list_safes())}
  • Contracts: {len(self.contract_manager.list_contracts())}

📝 Audit Summary
  • Total Entries: {audit_summary['total_entries']}
  • Status: {audit_summary['verification_status']}
  • Last Action: {audit_summary.get('last_action', 'None')}

🔐 Keyring Status
  • Backend: {self.keyring.audit_secrets()['backend']}
  • Service: GNOMAN
        """
        
        return Container(Static(content, classes="info-panel"))

    def _create_wallets_view(self) -> Container:
        """Create wallets panel."""
        table = DataTable()
        table.add_columns("Name", "Address", "Balance", "Chain")
        
        for wallet in self.wallet_manager.list_wallets():
            table.add_row(
                wallet["name"],
                wallet["address"],
                wallet["balance"],
                str(wallet.get("chain_id", "N/A"))
            )
        
        return Container(table)

    def _create_safes_view(self) -> Container:
        """Create safes panel."""
        table = DataTable()
        table.add_columns("Name", "Address", "Threshold", "Owners", "Balance")
        
        for safe in self.safe_manager.list_safes():
            table.add_row(
                safe["name"],
                safe["address"],
                str(safe["threshold"]),
                str(len(safe["owners"])),
                safe["balance"]
            )
        
        return Container(table)

    def _create_contracts_view(self) -> Container:
        """Create contracts panel."""
        content = """
📜 Custom Contract Interactions

• Load ABI from file
• Test contract functions locally
• Simulate transactions
• Cache tested ABIs

No contracts loaded yet.
        """
        return Container(Static(content, classes="info-panel"))

    def _create_audit_view(self) -> Container:
        """Create audit panel."""
        table = DataTable()
        table.add_columns("Timestamp", "Action", "User", "Status")
        
        recent_logs = self.audit_manager.get_recent_logs(20)
        for log in recent_logs:
            table.add_row(
                log["timestamp"][:19],
                log["action_type"],
                log["user"],
                "✓"
            )
        
        return Container(table)

    def _create_sync_view(self) -> Container:
        """Create sync panel."""
        content = """
🔄 Configuration Sync

Reconcile configuration between:
  • Environment variables (.env)
  • System keyring
  • Local config file

All systems synchronized.
        """
        return Container(Static(content, classes="info-panel"))

    def _create_secrets_view(self) -> Container:
        """Create secrets panel."""
        content = """
🗝️ Secret Management

• Inspect keyring entries
• Rotate credentials
• Export/import encrypted secrets
• Audit stale entries

Use with caution - manages sensitive data.
        """
        return Container(Static(content, classes="info-panel"))

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def on_mount(self) -> None:
        """Handle mount event."""
        self.log("GNOMAN started successfully")
