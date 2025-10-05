"""Tests for audit manager."""
import pytest
from gnoman.core.audit_manager import AuditManager
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_log_dir():
    """Create temporary log directory."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_log_action(temp_log_dir):
    """Test logging an action."""
    audit = AuditManager(temp_log_dir)
    
    hash1 = audit.log_action("test_action", {"key": "value"}, "testuser")
    
    assert hash1 is not None
    assert len(hash1) == 64  # SHA256 hex length
    
    logs = audit.get_recent_logs(1)
    assert len(logs) == 1
    assert logs[0]["action_type"] == "test_action"
    assert logs[0]["user"] == "testuser"


def test_log_chain(temp_log_dir):
    """Test log chain integrity."""
    audit = AuditManager(temp_log_dir)
    
    hash1 = audit.log_action("action1", {}, "user1")
    hash2 = audit.log_action("action2", {}, "user2")
    hash3 = audit.log_action("action3", {}, "user3")
    
    logs = audit.get_recent_logs(3)
    
    # Verify chain
    assert logs[0]["prev_hash"] == "genesis"
    assert logs[1]["prev_hash"] == hash1
    assert logs[2]["prev_hash"] == hash2


def test_verify_chain(temp_log_dir):
    """Test chain verification."""
    audit = AuditManager(temp_log_dir)
    
    audit.log_action("action1", {}, "user1")
    audit.log_action("action2", {}, "user2")
    
    result = audit.verify_chain()
    
    assert result["status"] == "ok"
    assert result["entries"] == 2


def test_get_summary(temp_log_dir):
    """Test getting audit summary."""
    audit = AuditManager(temp_log_dir)
    
    audit.log_action("wallet_created", {}, "user1")
    audit.log_action("safe_loaded", {}, "user2")
    
    summary = audit.get_summary()
    
    assert summary["total_entries"] == 2
    assert summary["verification_status"] == "ok"
    assert summary["last_action"] == "safe_loaded"


def test_export_logs(temp_log_dir):
    """Test exporting logs."""
    audit = AuditManager(temp_log_dir)
    
    audit.log_action("action1", {}, "user1")
    audit.log_action("action2", {}, "user2")
    
    logs = audit.export_logs()
    
    assert len(logs) == 2
    assert logs[0]["action_type"] == "action1"
    assert logs[1]["action_type"] == "action2"


def test_empty_audit(temp_log_dir):
    """Test audit manager with no logs."""
    audit = AuditManager(temp_log_dir)
    
    summary = audit.get_summary()
    assert summary["total_entries"] == 0
    
    logs = audit.get_recent_logs(10)
    assert len(logs) == 0
    
    result = audit.verify_chain()
    assert result["status"] == "ok"
