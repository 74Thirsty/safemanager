# GNOMAN Quick Start Guide

## Installation

```bash
# Install from source
git clone https://github.com/74Thirsty/safemanager.git
cd safemanager
pip install -r requirements.txt
pip install -e .
```

## Running GNOMAN

```bash
# Start the interactive console
gnoman

# Or run directly with Python
python -m gnoman.main
```

## First Run

On first run, GNOMAN will:
1. Display an animated splash screen
2. Initialize configuration at `~/.gnoman/`
3. Set up data directories
4. Connect to the system keyring
5. Load the main dashboard

## Using the Dashboard

### Navigation
- Use `Tab` and `Shift+Tab` to navigate between tabs
- Use arrow keys to navigate within tables
- Press `q` to quit
- Press `d` to toggle dark mode

### Available Tabs

#### 1. Wallets Tab
**Purpose**: Manage Ethereum wallets with secure private key storage

**Features**:
- Create new wallets
- Import existing wallets
- View wallet balances across multiple chains
- Secure private key storage in system keyring

**Keyboard Shortcuts**:
- `n` - Create new wallet
- `r` - Refresh balances
- `d` - Delete selected wallet

**Workflow**:
1. Press `n` to create a new wallet
2. The wallet is automatically generated and secured
3. Private key is encrypted and stored in keyring
4. Select wallet to view details

#### 2. Safes Tab
**Purpose**: Track and manage Gnosis Safe multisig wallets

**Features**:
- Track multiple Safe addresses
- View owners and threshold settings
- Monitor Safe balances
- Track pending transactions

**Keyboard Shortcuts**:
- `n` - Add Safe to track
- `r` - Refresh Safe data
- `d` - Delete Safe from tracking

**Workflow**:
1. Press `n` to add a Safe
2. Enter the Safe address
3. System fetches owners and threshold
4. View detailed Safe information

#### 3. Contracts Tab
**Purpose**: Manage smart contract ABIs and metadata

**Features**:
- Store contract addresses and ABIs
- Track contract verification status
- Support for proxy contracts
- Multi-chain contract tracking

**Keyboard Shortcuts**:
- `n` - Add contract
- `v` - View ABI
- `r` - Refresh contracts
- `d` - Delete contract

**Workflow**:
1. Press `n` to add a contract
2. Enter contract address
3. Optionally import ABI
4. View contract details and functions

#### 4. Audit Tab
**Purpose**: Security event logging and monitoring

**Features**:
- Automatic event logging
- Severity-based filtering
- Detailed event tracking
- Historical audit trail

**Keyboard Shortcuts**:
- `r` - Refresh audit log
- `c` - Clear logs (with confirmation)

**Severity Levels**:
- Info: General information
- Warning: Potential issues
- Error: Operation failures
- Critical: Security concerns

#### 5. Sync Tab
**Purpose**: Synchronize blockchain data

**Features**:
- Batch synchronization
- Individual component sync
- Progress tracking
- Last sync timestamps

**Keyboard Shortcuts**:
- `s` - Sync all data
- `w` - Sync wallets only
- `m` - Sync Safes only

**Workflow**:
1. Press `s` to sync all data
2. Watch progress bar
3. View last sync times
4. Individual components can be synced separately

#### 6. Secrets Tab
**Purpose**: Secure credential management

**Features**:
- System keyring integration
- Encrypted storage
- Service-based organization
- Secure private key storage

**Keyboard Shortcuts**:
- `n` - Add new secret
- `c` - Copy to clipboard
- `r` - Refresh list
- `d` - Delete secret

**Security Notes**:
- Secrets are never displayed in UI
- All storage uses system keyring
- Private keys are encrypted
- Automatic clipboard clearing

## Configuration

### Config File Location
`~/.gnoman/config.yaml`

### Example Configuration

```yaml
data_dir: ~/.gnoman
keyring_service: gnoman
default_chain_id: 1
theme: dark
auto_save: true
chains:
  1:
    chain_id: 1
    name: Ethereum Mainnet
    rpc_url: https://eth.llamarpc.com
    explorer_url: https://etherscan.io
    currency_symbol: ETH
```

### Adding Custom Networks

Edit `~/.gnoman/config.yaml` and add your network:

```yaml
chains:
  42161:
    chain_id: 42161
    name: Arbitrum One
    rpc_url: https://arb1.arbitrum.io/rpc
    explorer_url: https://arbiscan.io
    currency_symbol: ETH
```

## Data Storage

All data is stored locally at `~/.gnoman/`:

```
~/.gnoman/
├── config.yaml          # Application configuration
├── wallets/            # Wallet data (addresses, metadata)
├── safes/              # Safe multisig data
├── contracts/          # Contract ABIs and metadata
└── audits/             # Security audit logs
```

**Note**: Private keys are stored in the system keyring, NOT in files.

## Demo Mode

Run the included demo to see all features:

```bash
python demo.py
```

This will:
- Create sample wallet
- Create sample Safe
- Create sample contract
- Generate audit log entries
- Display data summary

## Security Best Practices

1. **Private Keys**: Never share private keys. They're encrypted in keyring.
2. **Backups**: Regularly backup `~/.gnoman/` directory
3. **Audit Logs**: Review audit logs for suspicious activity
4. **Network Selection**: Double-check chain ID before transactions
5. **Safe Thresholds**: Use appropriate threshold for multisigs

## Troubleshooting

### Application won't start
```bash
# Check Python version (requires 3.9+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Keyring errors
```bash
# Install system keyring support
# Ubuntu/Debian:
sudo apt-get install gnome-keyring

# macOS: Built-in
# Windows: Built-in
```

### Web3 connection issues
- Check RPC URL in config
- Verify network connectivity
- Try alternative RPC providers

### Data directory permissions
```bash
# Fix permissions
chmod 700 ~/.gnoman
chmod 600 ~/.gnoman/config.yaml
```

## Advanced Usage

### Custom RPC Endpoints

Add Infura or Alchemy endpoints:

```yaml
chains:
  1:
    rpc_url: https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

### Multiple Profiles

Use different data directories:

```bash
# Set custom data directory
export GNOMAN_DATA_DIR=~/.gnoman-prod
gnoman
```

### Batch Operations

Use the Python API for batch operations:

```python
from gnoman.models.config import AppConfig
from gnoman.utils.storage import DataStore

config = AppConfig.load()
storage = DataStore(config.data_dir)

# Batch update balances
wallets = storage.list_wallets()
for wallet in wallets:
    # Update logic here
    storage.save_wallet(wallet)
```

## Integration Examples

### Web3.py Integration

```python
from gnoman.utils.web3_manager import Web3Manager
from gnoman.models.config import AppConfig

config = AppConfig.load()
web3_mgr = Web3Manager(config)

# Get Web3 instance
w3 = web3_mgr.get_web3(chain_id=1)

# Use Web3.py normally
block = w3.eth.get_block('latest')
```

### Keyring Integration

```python
from gnoman.utils.keyring_manager import KeyringManager

km = KeyringManager("gnoman")

# Store secret
km.store_secret("my-api-key", "secret-value")

# Retrieve secret
secret = km.get_secret("my-api-key")
```

## Support

- GitHub Issues: https://github.com/74Thirsty/safemanager/issues
- Documentation: See README.md
- Demo: Run `python demo.py`
