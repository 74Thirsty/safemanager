"""Dashboard screen with tabbed interface"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane, Label
from textual.containers import Container
from gnoman.tabs.wallets_tab import WalletsTab
from gnoman.tabs.safes_tab import SafesTab
from gnoman.tabs.contracts_tab import ContractsTab
from gnoman.tabs.audit_tab import AuditTab
from gnoman.tabs.sync_tab import SyncTab
from gnoman.tabs.secrets_tab import SecretsTab
from gnoman.models.config import AppConfig
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.utils.keyring_manager import KeyringManager


class Dashboard(Screen):
    """Main dashboard screen with tabbed navigation"""
    
    CSS = """
    Dashboard {
        background: $surface;
    }
    
    .tab-title {
        text-style: bold;
        color: $primary;
        padding: 1;
        text-align: center;
        background: $panel;
    }
    
    .controls {
        height: auto;
        padding: 1;
        background: $panel;
    }
    
    .details-panel {
        height: auto;
        padding: 1;
        margin-top: 1;
        border: solid $primary;
        background: $panel;
    }
    
    .status-panel {
        height: auto;
        padding: 1;
        margin-top: 1;
        border: solid $accent;
        background: $panel;
    }
    
    .section-title {
        text-style: bold;
        color: $accent;
        padding-bottom: 1;
    }
    
    .warning-text {
        color: $warning;
        text-style: italic;
        padding-top: 1;
    }
    
    DataTable {
        height: 1fr;
        margin-top: 1;
    }
    
    Button {
        margin-right: 1;
    }
    """
    
    def __init__(self, config: AppConfig, storage: DataStore, 
                 web3_manager: Web3Manager, keyring_manager: KeyringManager):
        super().__init__()
        self.config = config
        self.storage = storage
        self.web3_manager = web3_manager
        self.keyring_manager = keyring_manager
    
    def compose(self) -> ComposeResult:
        """Compose the dashboard layout"""
        yield Header(show_clock=True)
        
        with TabbedContent():
            with TabPane("Wallets", id="tab-wallets"):
                yield WalletsTab(
                    self.config, self.storage, 
                    self.web3_manager, self.keyring_manager
                )
            
            with TabPane("Safes", id="tab-safes"):
                yield SafesTab(
                    self.config, self.storage, self.web3_manager
                )
            
            with TabPane("Contracts", id="tab-contracts"):
                yield ContractsTab(
                    self.config, self.storage, self.web3_manager
                )
            
            with TabPane("Audit", id="tab-audit"):
                yield AuditTab(self.storage)
            
            with TabPane("Sync", id="tab-sync"):
                yield SyncTab(
                    self.config, self.storage, self.web3_manager
                )
            
            with TabPane("Secrets", id="tab-secrets"):
                yield SecretsTab(self.keyring_manager)
        
        yield Footer()
