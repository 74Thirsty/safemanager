"""Tests for ABI tools."""
import pytest
from gnoman.utils.abi_tools import ABITools
from pathlib import Path
import tempfile
import shutil
import json


@pytest.fixture
def temp_cache_dir():
    """Create temporary cache directory."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_abi():
    """Sample ABI for testing."""
    return [
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]


def test_parse_abi_string(temp_cache_dir, sample_abi):
    """Test parsing ABI from string."""
    tools = ABITools(temp_cache_dir)
    
    abi_str = json.dumps(sample_abi)
    parsed = tools.parse_abi_string(abi_str, "test_abi")
    
    assert parsed == sample_abi
    assert "test_abi" in tools.loaded_abis


def test_get_function_signature(temp_cache_dir, sample_abi):
    """Test getting function signature."""
    tools = ABITools(temp_cache_dir)
    
    sig = tools.get_function_signature(sample_abi, "balanceOf")
    
    assert sig is not None
    assert sig["name"] == "balanceOf"
    assert len(sig["inputs"]) == 1


def test_get_nonexistent_function(temp_cache_dir, sample_abi):
    """Test getting nonexistent function."""
    tools = ABITools(temp_cache_dir)
    
    sig = tools.get_function_signature(sample_abi, "nonexistent")
    assert sig is None


def test_validate_inputs(temp_cache_dir, sample_abi):
    """Test input validation."""
    tools = ABITools(temp_cache_dir)
    
    sig = tools.get_function_signature(sample_abi, "balanceOf")
    
    # Valid input count
    assert tools.validate_inputs(sig, ["0x123"]) is True
    
    # Invalid input count
    assert tools.validate_inputs(sig, []) is False
    assert tools.validate_inputs(sig, ["0x123", "extra"]) is False


def test_load_abi_from_file(temp_cache_dir, sample_abi):
    """Test loading ABI from file."""
    tools = ABITools(temp_cache_dir)
    
    # Create temporary ABI file
    abi_file = temp_cache_dir / "test.json"
    with open(abi_file, 'w') as f:
        json.dump(sample_abi, f)
    
    loaded = tools.load_abi(str(abi_file), "from_file")
    
    assert loaded == sample_abi
    assert "from_file" in tools.loaded_abis


def test_list_cached_abis(temp_cache_dir, sample_abi):
    """Test listing cached ABIs."""
    tools = ABITools(temp_cache_dir)
    
    # Parse and cache an ABI
    abi_str = json.dumps(sample_abi)
    tools.parse_abi_string(abi_str, "cached_abi")
    
    cached = tools.list_cached_abis()
    assert "cached_abi" in cached


def test_get_cached_abi(temp_cache_dir, sample_abi):
    """Test retrieving cached ABI."""
    tools = ABITools(temp_cache_dir)
    
    # Cache an ABI
    abi_str = json.dumps(sample_abi)
    tools.parse_abi_string(abi_str, "to_retrieve")
    
    # Retrieve it
    retrieved = tools.get_cached_abi("to_retrieve")
    assert retrieved == sample_abi


def test_get_nonexistent_cached_abi(temp_cache_dir):
    """Test retrieving nonexistent cached ABI."""
    tools = ABITools(temp_cache_dir)
    
    retrieved = tools.get_cached_abi("nonexistent")
    assert retrieved is None
