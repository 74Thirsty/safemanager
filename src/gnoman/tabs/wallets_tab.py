"""Wallets tab for wallet management"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DataTable, Button, Input, Label, Static
from textual.binding import Binding
from typing import Optional
from gnoman.models.data_models import WalletModel
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.utils.keyring_manager import KeyringManager
from gnoman.models.config import AppConfig


class WalletsTab(Container):
    """Tab for managing Ethereum wallets"""
    
    BINDINGS = [
        Binding("n", "new_wallet", "New Wallet"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "delete_wallet", "Delete"),
    ]
    
    def __init__(self, config: AppConfig, storage: DataStore, web3_manager: Web3Manager, 
                 keyring_manager: KeyringManager):
        super().__init__()
        self.config = config
        self.storage = storage
        self.web3_manager = web3_manager
        self.keyring_manager = keyring_manager
        self.selected_wallet: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the wallets tab layout"""
        yield Label("Wallets Manager", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Button("New Wallet", id="btn-new-wallet", variant="primary")
            yield Button("Import Wallet", id="btn-import-wallet")
            yield Button("Refresh", id="btn-refresh")
            yield Button("Delete", id="btn-delete", variant="error")
        
        # Wallets table
        table = DataTable(id="wallets-table")
        table.cursor_type = "row"
        table.add_columns("Name", "Address", "Chain", "Balance", "Notes")
        yield table
        
        # Details section
        with Vertical(id="wallet-details", classes="details-panel"):
            yield Label("Wallet Details", classes="section-title")
            yield Static(id="wallet-info", markup=True)
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.refresh_wallets()
    
    def refresh_wallets(self) -> None:
        """Refresh the wallets list"""
        table = self.query_one("#wallets-table", DataTable)
        table.clear()
        
        wallets = self.storage.list_wallets()
        for wallet in wallets:
            # Update balance from blockchain
            balance = self.web3_manager.get_balance(wallet.address, wallet.chain_id)
            if balance:
                wallet.balance = balance
                self.storage.save_wallet(wallet)
            
            chain_name = self.config.chains.get(wallet.chain_id, None)
            chain_str = chain_name.name if chain_name else str(wallet.chain_id)
            
            table.add_row(
                wallet.name,
                wallet.address[:10] + "..." + wallet.address[-8:],
                chain_str,
                f"{wallet.balance[:10]} ETH",
                wallet.notes or "",
                key=wallet.name
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-new-wallet":
            self.action_new_wallet()
        elif event.button.id == "btn-import-wallet":
            self.action_import_wallet()
        elif event.button.id == "btn-refresh":
            self.action_refresh()
        elif event.button.id == "btn-delete":
            self.action_delete_wallet()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle wallet selection"""
        self.selected_wallet = str(event.row_key.value)
        self.show_wallet_details()
    
    def show_wallet_details(self) -> None:
        """Show details for selected wallet"""
        if not self.selected_wallet:
            return
        
        wallet = self.storage.load_wallet(self.selected_wallet)
        if not wallet:
            return
        
        info_widget = self.query_one("#wallet-info", Static)
        
        details = f"""[b]Name:[/b] {wallet.name}
[b]Address:[/b] {wallet.address}
[b]Chain ID:[/b] {wallet.chain_id}
[b]Balance:[/b] {wallet.balance} ETH
[b]Created:[/b] {wallet.created_at.strftime('%Y-%m-%d %H:%M:%S')}
[b]Notes:[/b] {wallet.notes or 'N/A'}
"""
        info_widget.update(details)
    
    def action_new_wallet(self) -> None:
        """Create a new wallet"""
        # Create new account
        account = self.web3_manager.create_account()
        
        # Generate default name
        wallet_count = len(self.storage.list_wallets())
        name = f"Wallet-{wallet_count + 1}"
        
        # Create wallet model
        wallet = WalletModel(
            name=name,
            address=account["address"],
            chain_id=self.config.default_chain_id,
            notes="Auto-generated wallet"
        )
        
        # Save wallet
        self.storage.save_wallet(wallet)
        
        # Store private key in keyring
        self.keyring_manager.store_secret(f"wallet_{name}_pk", account["private_key"])
        
        self.refresh_wallets()
        self.app.notify(f"Created new wallet: {name}")
    
    def action_import_wallet(self) -> None:
        """Import an existing wallet"""
        self.app.notify("Import wallet feature coming soon!")
    
    def action_refresh(self) -> None:
        """Refresh wallets list"""
        self.refresh_wallets()
        self.app.notify("Wallets refreshed")
    
    def action_delete_wallet(self) -> None:
        """Delete selected wallet"""
        if not self.selected_wallet:
            self.app.notify("No wallet selected", severity="warning")
            return
        
        self.storage.delete_wallet(self.selected_wallet)
        self.keyring_manager.delete_secret(f"wallet_{self.selected_wallet}_pk")
        self.selected_wallet = None
        
        self.refresh_wallets()
        self.app.notify("Wallet deleted")
