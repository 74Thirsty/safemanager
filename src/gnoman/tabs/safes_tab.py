"""Safes tab for Gnosis Safe multisig management"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DataTable, Button, Input, Label, Static
from textual.binding import Binding
from typing import Optional
from gnoman.models.data_models import SafeModel
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.utils.safe_manager import SafeManager
from gnoman.models.config import AppConfig


class SafesTab(Container):
    """Tab for managing Gnosis Safe multisigs"""
    
    BINDINGS = [
        Binding("n", "new_safe", "Add Safe"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "delete_safe", "Delete"),
    ]
    
    def __init__(self, config: AppConfig, storage: DataStore, web3_manager: Web3Manager):
        super().__init__()
        self.config = config
        self.storage = storage
        self.web3_manager = web3_manager
        self.selected_safe: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the safes tab layout"""
        yield Label("Gnosis Safe Multisigs", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Button("Add Safe", id="btn-new-safe", variant="primary")
            yield Button("Refresh", id="btn-refresh")
            yield Button("Delete", id="btn-delete", variant="error")
        
        # Safes table
        table = DataTable(id="safes-table")
        table.cursor_type = "row"
        table.add_columns("Name", "Address", "Chain", "Threshold", "Owners", "Balance")
        yield table
        
        # Details section
        with Vertical(id="safe-details", classes="details-panel"):
            yield Label("Safe Details", classes="section-title")
            yield Static(id="safe-info", markup=True)
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.refresh_safes()
    
    def refresh_safes(self) -> None:
        """Refresh the safes list"""
        table = self.query_one("#safes-table", DataTable)
        table.clear()
        
        safes = self.storage.list_safes()
        for safe in safes:
            # Update balance from blockchain
            balance = self.web3_manager.get_balance(safe.address, safe.chain_id)
            if balance:
                safe.balance = balance
                self.storage.save_safe(safe)
            
            chain_name = self.config.chains.get(safe.chain_id, None)
            chain_str = chain_name.name if chain_name else str(safe.chain_id)
            
            table.add_row(
                safe.name,
                safe.address[:10] + "..." + safe.address[-8:],
                chain_str,
                f"{safe.threshold}/{len(safe.owners)}",
                str(len(safe.owners)),
                f"{safe.balance[:10]} ETH",
                key=safe.name
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-new-safe":
            self.action_new_safe()
        elif event.button.id == "btn-refresh":
            self.action_refresh()
        elif event.button.id == "btn-delete":
            self.action_delete_safe()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle safe selection"""
        self.selected_safe = str(event.row_key.value)
        self.show_safe_details()
    
    def show_safe_details(self) -> None:
        """Show details for selected safe"""
        if not self.selected_safe:
            return
        
        safe = self.storage.load_safe(self.selected_safe)
        if not safe:
            return
        
        info_widget = self.query_one("#safe-info", Static)
        
        owners_str = "\n".join([f"  • {owner}" for owner in safe.owners]) if safe.owners else "N/A"
        
        details = f"""[b]Name:[/b] {safe.name}
[b]Address:[/b] {safe.address}
[b]Chain ID:[/b] {safe.chain_id}
[b]Threshold:[/b] {safe.threshold}/{len(safe.owners)}
[b]Nonce:[/b] {safe.nonce}
[b]Balance:[/b] {safe.balance} ETH
[b]Created:[/b] {safe.created_at.strftime('%Y-%m-%d %H:%M:%S')}
[b]Owners:[/b]
{owners_str}
[b]Notes:[/b] {safe.notes or 'N/A'}
"""
        info_widget.update(details)
    
    def action_new_safe(self) -> None:
        """Add a new Safe to track"""
        self.app.notify("Add Safe feature requires Safe address input. Coming soon!")
    
    def action_refresh(self) -> None:
        """Refresh safes list"""
        self.refresh_safes()
        self.app.notify("Safes refreshed")
    
    def action_delete_safe(self) -> None:
        """Delete selected safe"""
        if not self.selected_safe:
            self.app.notify("No Safe selected", severity="warning")
            return
        
        self.storage.delete_safe(self.selected_safe)
        self.selected_safe = None
        
        self.refresh_safes()
        self.app.notify("Safe deleted")
