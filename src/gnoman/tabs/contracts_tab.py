"""Contracts tab for smart contract and ABI management"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DataTable, Button, Label, Static
from textual.binding import Binding
from typing import Optional
from gnoman.models.data_models import ContractModel
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.models.config import AppConfig


class ContractsTab(Container):
    """Tab for managing smart contracts and ABIs"""
    
    BINDINGS = [
        Binding("n", "new_contract", "Add Contract"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "delete_contract", "Delete"),
        Binding("v", "view_abi", "View ABI"),
    ]
    
    def __init__(self, config: AppConfig, storage: DataStore, web3_manager: Web3Manager):
        super().__init__()
        self.config = config
        self.storage = storage
        self.web3_manager = web3_manager
        self.selected_contract: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the contracts tab layout"""
        yield Label("Smart Contracts & ABIs", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Button("Add Contract", id="btn-new-contract", variant="primary")
            yield Button("View ABI", id="btn-view-abi")
            yield Button("Refresh", id="btn-refresh")
            yield Button("Delete", id="btn-delete", variant="error")
        
        # Contracts table
        table = DataTable(id="contracts-table")
        table.cursor_type = "row"
        table.add_columns("Name", "Address", "Chain", "Verified", "Implementation", "Notes")
        yield table
        
        # Details section
        with Vertical(id="contract-details", classes="details-panel"):
            yield Label("Contract Details", classes="section-title")
            yield Static(id="contract-info", markup=True)
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.refresh_contracts()
    
    def refresh_contracts(self) -> None:
        """Refresh the contracts list"""
        table = self.query_one("#contracts-table", DataTable)
        table.clear()
        
        contracts = self.storage.list_contracts()
        for contract in contracts:
            # Verify it's actually a contract
            is_contract = self.web3_manager.is_contract(contract.address, contract.chain_id)
            
            chain_name = self.config.chains.get(contract.chain_id, None)
            chain_str = chain_name.name if chain_name else str(contract.chain_id)
            
            verified_str = "✓" if contract.verified else "✗"
            impl_str = contract.implementation[:10] + "..." if contract.implementation else "N/A"
            
            table.add_row(
                contract.name,
                contract.address[:10] + "..." + contract.address[-8:],
                chain_str,
                verified_str,
                impl_str,
                contract.notes or "",
                key=contract.name
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-new-contract":
            self.action_new_contract()
        elif event.button.id == "btn-view-abi":
            self.action_view_abi()
        elif event.button.id == "btn-refresh":
            self.action_refresh()
        elif event.button.id == "btn-delete":
            self.action_delete_contract()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle contract selection"""
        self.selected_contract = str(event.row_key.value)
        self.show_contract_details()
    
    def show_contract_details(self) -> None:
        """Show details for selected contract"""
        if not self.selected_contract:
            return
        
        contract = self.storage.load_contract(self.selected_contract)
        if not contract:
            return
        
        info_widget = self.query_one("#contract-info", Static)
        
        abi_count = len(contract.abi) if contract.abi else 0
        
        details = f"""[b]Name:[/b] {contract.name}
[b]Address:[/b] {contract.address}
[b]Chain ID:[/b] {contract.chain_id}
[b]Verified:[/b] {contract.verified}
[b]Implementation:[/b] {contract.implementation or 'N/A'}
[b]ABI Functions:[/b] {abi_count}
[b]Created:[/b] {contract.created_at.strftime('%Y-%m-%d %H:%M:%S')}
[b]Notes:[/b] {contract.notes or 'N/A'}
"""
        info_widget.update(details)
    
    def action_new_contract(self) -> None:
        """Add a new contract"""
        self.app.notify("Add Contract feature requires address input. Coming soon!")
    
    def action_view_abi(self) -> None:
        """View ABI for selected contract"""
        if not self.selected_contract:
            self.app.notify("No contract selected", severity="warning")
            return
        
        contract = self.storage.load_contract(self.selected_contract)
        if not contract:
            return
        
        if not contract.abi:
            self.app.notify("No ABI available for this contract", severity="warning")
            return
        
        self.app.notify(f"ABI has {len(contract.abi)} functions")
    
    def action_refresh(self) -> None:
        """Refresh contracts list"""
        self.refresh_contracts()
        self.app.notify("Contracts refreshed")
    
    def action_delete_contract(self) -> None:
        """Delete selected contract"""
        if not self.selected_contract:
            self.app.notify("No contract selected", severity="warning")
            return
        
        self.storage.delete_contract(self.selected_contract)
        self.selected_contract = None
        
        self.refresh_contracts()
        self.app.notify("Contract deleted")
