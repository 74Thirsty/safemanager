# GNOMAN Mission-Control Console

A full-featured Textual-based desktop application for managing Ethereum wallets, Gnosis Safe multisigs, smart contracts, security audits, and secrets.

## Features

### 🔐 Wallets Manager
- Create and import Ethereum wallets
- Secure private key storage using system keyring
- Real-time balance tracking via Web3
- Multi-chain support (Ethereum, Polygon, testnets)

### 🏦 Safes Manager
- Track Gnosis Safe multisig wallets
- View owners, threshold, and nonce
- Monitor Safe balances across chains
- Integration with Safe-ETH library

### 📜 Contracts Manager
- Store and manage smart contract ABIs
- Track contract verification status
- Support for proxy contracts
- Multi-chain contract tracking

### 🔍 Audit Log
- Security event logging
- Severity-based filtering
- Detailed event tracking
- User action auditing

### 🔄 Sync Manager
- Synchronize wallet balances
- Update Safe information
- Batch synchronization
- Progress tracking

### 🔑 Secrets Manager
- Secure credential storage
- System keyring integration
- Encrypted private key storage
- Service-based secret organization

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/74Thirsty/safemanager.git
cd safemanager

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

### Running the application

```bash
gnoman
```

### Keyboard Shortcuts

- `q` - Quit application
- `d` - Toggle dark mode
- `n` - New item (context-dependent)
- `r` - Refresh current view
- `Tab` - Navigate between tabs
- `Shift+Tab` - Navigate backward between tabs

### Configuration

The application stores its configuration and data in `~/.gnoman/`:

```
~/.gnoman/
├── config.yaml          # Application configuration
├── wallets/            # Wallet data
├── safes/              # Safe multisig data
├── contracts/          # Contract and ABI data
└── audits/             # Audit logs
```

### Example Configuration

The default configuration includes common Ethereum networks:

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
  137:
    chain_id: 137
    name: Polygon Mainnet
    rpc_url: https://polygon-rpc.com
    explorer_url: https://polygonscan.com
    currency_symbol: MATIC
```

## Architecture

### Core Components

- **Textual Framework**: Modern terminal UI framework
- **Web3.py**: Ethereum blockchain interaction
- **Safe-ETH-py**: Gnosis Safe integration
- **Keyring**: Secure credential storage
- **Pydantic**: Data validation and models

### Project Structure

```
src/gnoman/
├── core/
│   ├── splash.py       # Splash screen
│   └── dashboard.py    # Main dashboard
├── tabs/
│   ├── wallets_tab.py  # Wallets management
│   ├── safes_tab.py    # Safes management
│   ├── contracts_tab.py # Contracts management
│   ├── audit_tab.py    # Audit logging
│   ├── sync_tab.py     # Data synchronization
│   └── secrets_tab.py  # Secrets management
├── models/
│   ├── data_models.py  # Data models
│   └── config.py       # Configuration
├── utils/
│   ├── keyring_manager.py  # Keyring operations
│   ├── web3_manager.py     # Web3 operations
│   ├── safe_manager.py     # Safe operations
│   └── storage.py          # Data persistence
└── main.py             # Application entry point
```

## Security

- Private keys are encrypted and stored in the system keyring
- Secrets are never displayed in the UI
- All sensitive operations are logged in the audit log
- Multi-factor authentication support (coming soon)

## Development

### Setting up development environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
python -m gnoman.main
```

### Running with Textual DevTools

```bash
# Install textual devtools
pip install textual-dev

# Run with console
textual run --dev gnoman.main:GnomanApp
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.