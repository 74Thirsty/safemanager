"""Audit manager for GNOMAN."""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import hashlib
from datetime import datetime


class AuditManager:
    """Manager for audit logging and verification."""

    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize audit manager.
        
        Args:
            log_dir: Directory for audit logs
        """
        self.log_dir = log_dir or Path.home() / ".gnoman" / "audit_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "audit.jsonl"
        self.last_hash: Optional[str] = None
        self._load_last_hash()

    def _load_last_hash(self) -> None:
        """Load the last hash from log file."""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    self.last_hash = last_entry.get("hash")

    def log_action(
        self,
        action_type: str,
        details: Dict[str, Any],
        user: str = "system"
    ) -> str:
        """Log an action to the audit trail.
        
        Args:
            action_type: Type of action (e.g., "wallet_created", "safe_loaded")
            details: Action details
            user: User performing the action
            
        Returns:
            Hash of the log entry
        """
        timestamp = datetime.utcnow().isoformat()
        
        entry = {
            "timestamp": timestamp,
            "action_type": action_type,
            "user": user,
            "details": details,
            "prev_hash": self.last_hash or "genesis"
        }
        
        # Calculate hash
        entry_str = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_str.encode()).hexdigest()
        entry["hash"] = entry_hash
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        self.last_hash = entry_hash
        return entry_hash

    def get_recent_logs(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent log entries.
        
        Args:
            count: Number of recent entries to retrieve
            
        Returns:
            List of log entries
        """
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        recent = lines[-count:] if len(lines) > count else lines
        return [json.loads(line) for line in recent]

    def verify_chain(self) -> Dict[str, Any]:
        """Verify the integrity of the audit log chain.
        
        Returns:
            Verification result dictionary
        """
        if not self.log_file.exists():
            return {"status": "ok", "entries": 0, "message": "No logs to verify"}
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        prev_hash = "genesis"
        for i, line in enumerate(lines):
            entry = json.loads(line)
            
            # Verify previous hash matches
            if entry.get("prev_hash") != prev_hash:
                return {
                    "status": "error",
                    "entry": i,
                    "message": f"Hash chain broken at entry {i}"
                }
            
            # Recalculate and verify current hash
            stored_hash = entry.pop("hash")
            entry_str = json.dumps(entry, sort_keys=True)
            calculated_hash = hashlib.sha256(entry_str.encode()).hexdigest()
            
            if calculated_hash != stored_hash:
                return {
                    "status": "error",
                    "entry": i,
                    "message": f"Hash mismatch at entry {i}"
                }
            
            prev_hash = stored_hash
        
        return {
            "status": "ok",
            "entries": len(lines),
            "message": "All entries verified"
        }

    def export_logs(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Export logs within date range.
        
        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            
        Returns:
            List of log entries
        """
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        logs = [json.loads(line) for line in lines]
        
        # Filter by date if specified
        if start_date or end_date:
            filtered = []
            for log in logs:
                timestamp = log.get("timestamp", "")
                if start_date and timestamp < start_date:
                    continue
                if end_date and timestamp > end_date:
                    continue
                filtered.append(log)
            return filtered
        
        return logs

    def get_summary(self) -> Dict[str, Any]:
        """Get audit log summary.
        
        Returns:
            Summary dictionary
        """
        if not self.log_file.exists():
            return {
                "total_entries": 0,
                "verification_status": "ok",
                "last_action": None
            }
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        last_entry = json.loads(lines[-1]) if lines else None
        
        return {
            "total_entries": len(lines),
            "verification_status": self.verify_chain()["status"],
            "last_action": last_entry.get("action_type") if last_entry else None,
            "last_timestamp": last_entry.get("timestamp") if last_entry else None
        }
