"""Sync tab for data synchronization features"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Label, Static, ProgressBar
from textual.binding import Binding
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.models.config import AppConfig
from datetime import datetime


class SyncTab(Container):
    """Tab for data synchronization and blockchain state updates"""
    
    BINDINGS = [
        Binding("s", "sync_all", "Sync All"),
        Binding("w", "sync_wallets", "Sync Wallets"),
        Binding("m", "sync_safes", "Sync Safes"),
    ]
    
    def __init__(self, config: AppConfig, storage: DataStore, web3_manager: Web3Manager):
        super().__init__()
        self.config = config
        self.storage = storage
        self.web3_manager = web3_manager
        self.last_sync: dict = {}
    
    def compose(self) -> ComposeResult:
        """Compose the sync tab layout"""
        yield Label("Data Synchronization", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Button("Sync All", id="btn-sync-all", variant="primary")
            yield Button("Sync Wallets", id="btn-sync-wallets")
            yield Button("Sync Safes", id="btn-sync-safes")
            yield Button("Sync Contracts", id="btn-sync-contracts")
        
        # Sync status
        with Vertical(id="sync-status", classes="status-panel"):
            yield Label("Sync Status", classes="section-title")
            yield Static(id="sync-info", markup=True)
            yield ProgressBar(id="sync-progress", total=100, show_eta=False)
        
        # Last sync times
        with Vertical(id="sync-history", classes="details-panel"):
            yield Label("Last Sync Times", classes="section-title")
            yield Static(id="sync-history-info", markup=True)
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.update_sync_status()
    
    def update_sync_status(self) -> None:
        """Update the sync status display"""
        info_widget = self.query_one("#sync-info", Static)
        history_widget = self.query_one("#sync-history-info", Static)
        
        wallets_count = len(self.storage.list_wallets())
        safes_count = len(self.storage.list_safes())
        contracts_count = len(self.storage.list_contracts())
        
        status = f"""[b]Wallets:[/b] {wallets_count} tracked
[b]Safes:[/b] {safes_count} tracked
[b]Contracts:[/b] {contracts_count} tracked
[b]Status:[/b] Ready for synchronization
"""
        info_widget.update(status)
        
        # Update last sync times
        history_lines = []
        for key, timestamp in self.last_sync.items():
            history_lines.append(f"[b]{key}:[/b] {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if history_lines:
            history_widget.update("\n".join(history_lines))
        else:
            history_widget.update("No synchronization performed yet")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-sync-all":
            self.action_sync_all()
        elif event.button.id == "btn-sync-wallets":
            self.action_sync_wallets()
        elif event.button.id == "btn-sync-safes":
            self.action_sync_safes()
        elif event.button.id == "btn-sync-contracts":
            self.action_sync_contracts()
    
    def action_sync_all(self) -> None:
        """Sync all data"""
        progress = self.query_one("#sync-progress", ProgressBar)
        progress.update(progress=0)
        
        self.app.notify("Starting full synchronization...")
        
        # Sync wallets
        self.sync_wallets_data()
        progress.update(progress=33)
        
        # Sync safes
        self.sync_safes_data()
        progress.update(progress=66)
        
        # Sync contracts
        self.sync_contracts_data()
        progress.update(progress=100)
        
        self.last_sync["All"] = datetime.now()
        self.update_sync_status()
        self.app.notify("Full synchronization completed!")
    
    def action_sync_wallets(self) -> None:
        """Sync wallets data"""
        self.sync_wallets_data()
        self.last_sync["Wallets"] = datetime.now()
        self.update_sync_status()
        self.app.notify("Wallets synchronized")
    
    def action_sync_safes(self) -> None:
        """Sync safes data"""
        self.sync_safes_data()
        self.last_sync["Safes"] = datetime.now()
        self.update_sync_status()
        self.app.notify("Safes synchronized")
    
    def action_sync_contracts(self) -> None:
        """Sync contracts data"""
        self.sync_contracts_data()
        self.last_sync["Contracts"] = datetime.now()
        self.update_sync_status()
        self.app.notify("Contracts synchronized")
    
    def sync_wallets_data(self) -> None:
        """Synchronize wallet balances and data"""
        wallets = self.storage.list_wallets()
        for wallet in wallets:
            balance = self.web3_manager.get_balance(wallet.address, wallet.chain_id)
            if balance:
                wallet.balance = balance
                self.storage.save_wallet(wallet)
    
    def sync_safes_data(self) -> None:
        """Synchronize Safe balances and data"""
        safes = self.storage.list_safes()
        for safe in safes:
            balance = self.web3_manager.get_balance(safe.address, safe.chain_id)
            if balance:
                safe.balance = balance
            
            nonce = self.web3_manager.get_transaction_count(safe.address, safe.chain_id)
            if nonce is not None:
                safe.nonce = nonce
            
            self.storage.save_safe(safe)
    
    def sync_contracts_data(self) -> None:
        """Synchronize contract verification status"""
        contracts = self.storage.list_contracts()
        for contract in contracts:
            # Check if it's still a contract
            is_contract = self.web3_manager.is_contract(contract.address, contract.chain_id)
            if not is_contract:
                self.app.notify(f"Warning: {contract.name} is not a contract", severity="warning")
