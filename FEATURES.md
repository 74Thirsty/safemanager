# GNOMAN Features Documentation

## Overview

GNOMAN is a production-ready, full-featured mission-control console for managing Ethereum wallets, Gnosis Safe multisigs, smart contracts, security audits, and secrets. Built with the Textual framework, it provides a powerful terminal UI with real blockchain integration.

## Core Components

### 1. Splash Screen
**Location**: `src/gnoman/core/splash.py`

**Features**:
- Animated ASCII art logo
- Loading state animations
- Smooth transition to dashboard
- Professional startup experience

**Implementation**:
- Uses Textual Screen API
- Async loading states
- Auto-transitions after initialization

---

### 2. Dashboard
**Location**: `src/gnoman/core/dashboard.py`

**Features**:
- Tabbed navigation interface
- Header with clock
- Footer with keyboard shortcuts
- Responsive layout
- Dark/Light theme support

**Components**:
- 6 integrated tabs
- Consistent styling
- Keyboard navigation

---

### 3. Wallets Tab
**Location**: `src/gnoman/tabs/wallets_tab.py`

**Features**:
- **Wallet Creation**: Generate new Ethereum wallets
- **Import Wallets**: Import existing wallets (coming soon)
- **Balance Tracking**: Real-time balance updates via Web3
- **Multi-Chain Support**: Works across Ethereum, Polygon, testnets
- **Secure Storage**: Private keys stored in system keyring
- **Wallet Details**: View full wallet information

**Data Model**:
```python
WalletModel(
    name: str,
    address: str,
    chain_id: int,
    balance: str,
    created_at: datetime,
    notes: Optional[str]
)
```

**Security**:
- Private keys encrypted with Fernet
- System keyring integration
- Never stored in plaintext
- Passphrase protection

**Keyboard Shortcuts**:
- `n` - New wallet
- `r` - Refresh balances
- `d` - Delete wallet

---

### 4. Safes Tab
**Location**: `src/gnoman/tabs/safes_tab.py`

**Features**:
- **Safe Tracking**: Track multiple Gnosis Safe addresses
- **Owner Display**: View all Safe owners
- **Threshold Monitoring**: Display threshold requirements
- **Balance Updates**: Real-time Safe balance tracking
- **Nonce Tracking**: Monitor transaction nonces
- **Multi-Chain**: Support for Safes on different chains

**Data Model**:
```python
SafeModel(
    name: str,
    address: str,
    chain_id: int,
    threshold: int,
    owners: List[str],
    balance: str,
    nonce: int,
    created_at: datetime,
    notes: Optional[str]
)
```

**Integration**:
- Web3 for balance queries
- Address validation
- Safe metadata storage

**Keyboard Shortcuts**:
- `n` - Add Safe
- `r` - Refresh Safe data
- `d` - Delete Safe

---

### 5. Contracts Tab
**Location**: `src/gnoman/tabs/contracts_tab.py`

**Features**:
- **ABI Storage**: Store and manage contract ABIs
- **Verification Status**: Track contract verification
- **Proxy Support**: Implementation address tracking
- **Multi-Chain**: Track contracts across networks
- **Contract Detection**: Verify address is actually a contract

**Data Model**:
```python
ContractModel(
    name: str,
    address: str,
    chain_id: int,
    abi: List[Dict[str, Any]],
    implementation: Optional[str],
    verified: bool,
    created_at: datetime,
    notes: Optional[str]
)
```

**Features**:
- ABI import/export
- Function signature display
- Implementation tracking for proxies
- Contract code verification

**Keyboard Shortcuts**:
- `n` - Add contract
- `v` - View ABI
- `r` - Refresh contracts
- `d` - Delete contract

---

### 6. Audit Tab
**Location**: `src/gnoman/tabs/audit_tab.py`

**Features**:
- **Event Logging**: Automatic security event logging
- **Severity Filtering**: Filter by info, warning, error, critical
- **Historical Data**: 30-day audit trail
- **Detailed Events**: Full event details and context
- **User Tracking**: Track which user performed actions

**Data Model**:
```python
AuditModel(
    timestamp: datetime,
    event_type: str,
    target: str,
    details: Dict[str, Any],
    severity: str,  # info, warning, error, critical
    user: Optional[str]
)
```

**Severity Levels**:
- **Info**: General information
- **Warning**: Potential issues
- **Error**: Operation failures
- **Critical**: Security concerns

**Storage**:
- Daily log files (JSONL format)
- Append-only for integrity
- Easy to parse and analyze

**Keyboard Shortcuts**:
- `r` - Refresh log
- `c` - Clear logs (with confirmation)

---

### 7. Sync Tab
**Location**: `src/gnoman/tabs/sync_tab.py`

**Features**:
- **Batch Sync**: Sync all data at once
- **Selective Sync**: Sync wallets, Safes, or contracts individually
- **Progress Tracking**: Visual progress bar
- **Last Sync Times**: Track when each component was synced
- **Balance Updates**: Update all wallet and Safe balances
- **Nonce Updates**: Update Safe nonces

**Operations**:
- Sync All: Update all components
- Sync Wallets: Update wallet balances
- Sync Safes: Update Safe data
- Sync Contracts: Verify contract status

**Keyboard Shortcuts**:
- `s` - Sync all
- `w` - Sync wallets
- `m` - Sync Safes

---

### 8. Secrets Tab
**Location**: `src/gnoman/tabs/secrets_tab.py`

**Features**:
- **Secure Storage**: System keyring integration
- **API Keys**: Store API keys and tokens
- **Private Keys**: Encrypted private key storage
- **Service Organization**: Organize by service
- **Clipboard Copy**: Copy secrets to clipboard
- **Never Display**: Secrets never shown in UI

**Data Model**:
```python
SecretModel(
    name: str,
    service: str,
    username: Optional[str],
    created_at: datetime,
    updated_at: datetime,
    notes: Optional[str]
)
```

**Security Features**:
- System keyring (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- Encrypted storage
- Auto-clear clipboard (coming soon)
- Audit log integration

**Keyboard Shortcuts**:
- `n` - New secret
- `c` - Copy to clipboard
- `r` - Refresh list
- `d` - Delete secret

---

## Utility Modules

### Web3 Manager
**Location**: `src/gnoman/utils/web3_manager.py`

**Features**:
- Multi-chain Web3 connection management
- Balance queries
- Transaction count (nonce) retrieval
- Contract code fetching
- Account creation
- Message signing
- PoA middleware for Polygon

**Supported Networks**:
- Ethereum Mainnet
- Goerli Testnet
- Sepolia Testnet
- Polygon Mainnet
- Custom RPC endpoints

---

### Keyring Manager
**Location**: `src/gnoman/utils/keyring_manager.py`

**Features**:
- System keyring integration
- Secret storage and retrieval
- Encrypted private key storage
- Passphrase-based encryption
- Secure key derivation (SHA256)

**Encryption**:
- Fernet symmetric encryption
- PBKDF2-like key derivation
- Base64 encoding for storage

---

### Storage Manager
**Location**: `src/gnoman/utils/storage.py`

**Features**:
- JSON-based data storage
- CRUD operations for all models
- Audit log management
- Directory structure management
- Auto-save functionality

**Storage Structure**:
```
~/.gnoman/
├── wallets/         # Wallet JSON files
├── safes/           # Safe JSON files
├── contracts/       # Contract JSON files
└── audits/          # Audit log files (JSONL)
```

---

### Safe Manager
**Location**: `src/gnoman/utils/safe_manager.py`

**Features**:
- Safe information retrieval
- Balance queries
- Pending transaction tracking
- Gas estimation

---

## Configuration

### AppConfig
**Location**: `src/gnoman/models/config.py`

**Features**:
- YAML-based configuration
- Multi-chain definitions
- Theme settings
- Auto-save preferences
- Data directory configuration

**Configuration Options**:
```yaml
data_dir: ~/.gnoman
keyring_service: gnoman
default_chain_id: 1
theme: dark
auto_save: true
chains:
  <chain_id>:
    chain_id: int
    name: str
    rpc_url: str
    explorer_url: str
    currency_symbol: str
```

---

## Data Models

### Validation
All models use Pydantic for:
- Type validation
- Address checksum validation
- Automatic serialization
- JSON schema generation

### Models
- **WalletModel**: Ethereum wallet data
- **SafeModel**: Gnosis Safe multisig data
- **ContractModel**: Smart contract and ABI data
- **AuditModel**: Security audit log entries
- **SecretModel**: Credential metadata
- **ChainConfig**: Blockchain network configuration
- **AppConfig**: Application settings

---

## Security Features

### 1. Private Key Protection
- Never stored in plaintext
- Encrypted with Fernet
- Stored in system keyring
- Passphrase protection

### 2. Audit Logging
- All operations logged
- Severity classification
- User tracking
- Append-only logs

### 3. Secrets Management
- System keyring integration
- Never displayed in UI
- Encrypted storage
- Service-based organization

### 4. Address Validation
- Checksum validation
- Automatic normalization
- Invalid address rejection

---

## Production-Ready Features

### 1. Error Handling
- Try-catch blocks throughout
- User-friendly error messages
- Graceful degradation
- Detailed error logging

### 2. Data Persistence
- JSON file storage
- Atomic writes
- Directory structure management
- Backup-friendly format

### 3. Configuration Management
- YAML configuration
- Environment variable support
- Default configurations
- Multi-profile support

### 4. User Interface
- Keyboard shortcuts
- Tab navigation
- Dark/Light themes
- Responsive layout
- Status notifications

### 5. Multi-Chain Support
- Configurable networks
- Custom RPC endpoints
- Explorer integration
- Chain-specific settings

---

## Future Enhancements

### Planned Features
- Transaction creation and signing
- Safe transaction proposals
- Multi-signature workflow
- Contract interaction UI
- ABI import from Etherscan
- Hardware wallet support
- QR code display
- Clipboard auto-clear
- Export/Import functionality
- Advanced search and filtering

### Integration Opportunities
- Etherscan API integration
- IPFS for ABI storage
- ENS name resolution
- Token balance tracking
- NFT display
- DeFi protocol integration

---

## Testing

### Manual Testing
Run the demo script:
```bash
python demo.py
```

### Core Component Tests
```bash
python -c "from gnoman.main import GnomanApp; print('✓ Main app import')"
python -c "from gnoman.models.config import AppConfig; print('✓ Config')"
python -c "from gnoman.utils.web3_manager import Web3Manager; print('✓ Web3')"
```

---

## Performance

### Optimizations
- Lazy Web3 connection initialization
- Cached blockchain data
- Efficient file I/O
- Minimal dependencies
- Async UI updates

### Resource Usage
- Low memory footprint
- Minimal CPU usage
- Fast startup time
- Responsive UI

---

## Deployment

### Installation
```bash
pip install -e .
```

### Running
```bash
gnoman
```

### Distribution
```bash
python setup.py sdist bdist_wheel
```

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/74Thirsty/safemanager/issues
- Documentation: See README.md and QUICKSTART.md
- Demo: Run `python demo.py`
