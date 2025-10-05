"""Secrets tab for secure credential management"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DataTable, Button, Label, Static, Input
from textual.binding import Binding
from typing import Optional
from gnoman.models.data_models import SecretModel
from gnoman.utils.keyring_manager import KeyringManager
from datetime import datetime


class SecretsTab(Container):
    """Tab for managing secrets and credentials"""
    
    BINDINGS = [
        Binding("n", "new_secret", "New Secret"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "delete_secret", "Delete"),
        Binding("c", "copy_secret", "Copy"),
    ]
    
    def __init__(self, keyring_manager: KeyringManager):
        super().__init__()
        self.keyring_manager = keyring_manager
        self.secrets: list = []  # List of secret metadata
        self.selected_secret: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the secrets tab layout"""
        yield Label("Secrets Manager", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Button("New Secret", id="btn-new-secret", variant="primary")
            yield Button("Refresh", id="btn-refresh")
            yield Button("Copy", id="btn-copy")
            yield Button("Delete", id="btn-delete", variant="error")
        
        # Secrets table
        table = DataTable(id="secrets-table")
        table.cursor_type = "row"
        table.add_columns("Name", "Service", "Username", "Created", "Updated")
        yield table
        
        # Details section
        with Vertical(id="secret-details", classes="details-panel"):
            yield Label("Secret Details", classes="section-title")
            yield Static(id="secret-info", markup=True)
            yield Label("⚠️ Secrets are stored securely in system keyring", 
                       classes="warning-text")
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.refresh_secrets()
    
    def refresh_secrets(self) -> None:
        """Refresh the secrets list"""
        table = self.query_one("#secrets-table", DataTable)
        table.clear()
        
        # In a real implementation, you'd store secret metadata separately
        # For now, we'll show some example entries
        example_secrets = [
            {
                "name": "example-api-key",
                "service": "Example API",
                "username": "admin",
                "created": datetime.now(),
                "updated": datetime.now()
            }
        ]
        
        for secret_meta in example_secrets:
            table.add_row(
                secret_meta["name"],
                secret_meta["service"],
                secret_meta["username"] or "N/A",
                secret_meta["created"].strftime("%Y-%m-%d"),
                secret_meta["updated"].strftime("%Y-%m-%d"),
                key=secret_meta["name"]
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-new-secret":
            self.action_new_secret()
        elif event.button.id == "btn-refresh":
            self.action_refresh()
        elif event.button.id == "btn-copy":
            self.action_copy_secret()
        elif event.button.id == "btn-delete":
            self.action_delete_secret()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle secret selection"""
        self.selected_secret = str(event.row_key.value)
        self.show_secret_details()
    
    def show_secret_details(self) -> None:
        """Show details for selected secret (without revealing the actual secret)"""
        if not self.selected_secret:
            return
        
        info_widget = self.query_one("#secret-info", Static)
        
        # Show metadata only, never display the actual secret
        details = f"""[b]Name:[/b] {self.selected_secret}
[b]Service:[/b] Example API
[b]Username:[/b] admin
[b]Created:[/b] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
[b]Updated:[/b] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[yellow]⚠️ Secret value is stored securely and not displayed[/yellow]
"""
        info_widget.update(details)
    
    def action_new_secret(self) -> None:
        """Add a new secret"""
        self.app.notify("New Secret feature requires input form. Coming soon!")
    
    def action_refresh(self) -> None:
        """Refresh secrets list"""
        self.refresh_secrets()
        self.app.notify("Secrets refreshed")
    
    def action_copy_secret(self) -> None:
        """Copy secret to clipboard"""
        if not self.selected_secret:
            self.app.notify("No secret selected", severity="warning")
            return
        
        # In a real implementation, you would:
        # 1. Retrieve the secret from keyring
        # 2. Copy it to clipboard
        # 3. Clear clipboard after a timeout
        self.app.notify("Copy to clipboard feature coming soon!")
    
    def action_delete_secret(self) -> None:
        """Delete selected secret"""
        if not self.selected_secret:
            self.app.notify("No secret selected", severity="warning")
            return
        
        success = self.keyring_manager.delete_secret(self.selected_secret)
        if success:
            self.selected_secret = None
            self.refresh_secrets()
            self.app.notify("Secret deleted")
        else:
            self.app.notify("Failed to delete secret", severity="error")
