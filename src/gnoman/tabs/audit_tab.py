"""Audit tab for security auditing and logging"""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DataTable, Button, Label, Static, Select
from textual.binding import Binding
from gnoman.models.data_models import AuditModel
from gnoman.utils.storage import DataStore
from datetime import datetime


class AuditTab(Container):
    """Tab for security auditing and event logging"""
    
    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("c", "clear", "Clear All"),
    ]
    
    def __init__(self, storage: DataStore):
        super().__init__()
        self.storage = storage
        self.severity_filter = "all"
    
    def compose(self) -> ComposeResult:
        """Compose the audit tab layout"""
        yield Label("Security Audit Log", classes="tab-title")
        
        with Horizontal(classes="controls"):
            yield Label("Filter by severity:")
            yield Select(
                [("All", "all"), ("Info", "info"), ("Warning", "warning"), 
                 ("Error", "error"), ("Critical", "critical")],
                value="all",
                id="severity-filter"
            )
            yield Button("Refresh", id="btn-refresh")
            yield Button("Clear All", id="btn-clear", variant="error")
        
        # Audit table
        table = DataTable(id="audit-table")
        table.cursor_type = "row"
        table.add_columns("Timestamp", "Event Type", "Target", "Severity", "User", "Details")
        yield table
        
        # Details section
        with Vertical(id="audit-details", classes="details-panel"):
            yield Label("Audit Details", classes="section-title")
            yield Static(id="audit-info", markup=True)
    
    def on_mount(self) -> None:
        """Handle mount event"""
        self.refresh_audits()
    
    def refresh_audits(self) -> None:
        """Refresh the audit log"""
        table = self.query_one("#audit-table", DataTable)
        table.clear()
        
        audits = self.storage.list_audits(days=30)  # Last 30 days
        
        for audit in audits:
            # Apply severity filter
            if self.severity_filter != "all" and audit.severity != self.severity_filter:
                continue
            
            timestamp_str = audit.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            details_preview = str(audit.details)[:30] + "..." if len(str(audit.details)) > 30 else str(audit.details)
            
            # Color code by severity
            severity_display = audit.severity.upper()
            if audit.severity == "critical":
                severity_display = f"[red]{severity_display}[/red]"
            elif audit.severity == "error":
                severity_display = f"[yellow]{severity_display}[/yellow]"
            elif audit.severity == "warning":
                severity_display = f"[orange]{severity_display}[/orange]"
            
            table.add_row(
                timestamp_str,
                audit.event_type,
                audit.target,
                severity_display,
                audit.user or "system",
                details_preview,
                key=timestamp_str
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "btn-refresh":
            self.action_refresh()
        elif event.button.id == "btn-clear":
            self.action_clear()
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle severity filter change"""
        if event.select.id == "severity-filter":
            self.severity_filter = str(event.value)
            self.refresh_audits()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle audit entry selection"""
        # Find the selected audit entry
        timestamp_str = str(event.row_key.value)
        audits = self.storage.list_audits(days=30)
        
        selected_audit = None
        for audit in audits:
            if audit.timestamp.strftime("%Y-%m-%d %H:%M:%S") == timestamp_str:
                selected_audit = audit
                break
        
        if selected_audit:
            self.show_audit_details(selected_audit)
    
    def show_audit_details(self, audit: AuditModel) -> None:
        """Show details for selected audit entry"""
        info_widget = self.query_one("#audit-info", Static)
        
        details_str = "\n".join([f"  {k}: {v}" for k, v in audit.details.items()])
        
        details = f"""[b]Timestamp:[/b] {audit.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
[b]Event Type:[/b] {audit.event_type}
[b]Target:[/b] {audit.target}
[b]Severity:[/b] {audit.severity.upper()}
[b]User:[/b] {audit.user or 'system'}
[b]Details:[/b]
{details_str}
"""
        info_widget.update(details)
    
    def action_refresh(self) -> None:
        """Refresh audit log"""
        self.refresh_audits()
        self.app.notify("Audit log refreshed")
    
    def action_clear(self) -> None:
        """Clear all audit logs"""
        self.app.notify("Clear audit log feature requires confirmation. Coming soon!")
    
    def log_event(self, event_type: str, target: str, details: dict, 
                  severity: str = "info", user: str = None) -> None:
        """Log a new audit event"""
        audit = AuditModel(
            event_type=event_type,
            target=target,
            details=details,
            severity=severity,
            user=user
        )
        self.storage.log_audit(audit)
        self.refresh_audits()
