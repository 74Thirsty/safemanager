# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/74Thirsty/safemanager.git
cd safemanager

# Install dependencies
pip install -e .
```

## Running GNOMAN

### Interactive TUI Dashboard

```bash
gnoman run
```

This launches the full text-based user interface with tabs for:
- Overview (network status, metrics)
- Wallets (create, import, manage)
- Safes (load and interact with Gnosis Safe contracts)
- Contracts (custom ABI interactions)
- Audit (view logs and verify integrity)
- Sync (reconcile configurations)
- Secrets (keyring management)

### CLI Commands

#### Wallet Operations

```bash
# Generate a new wallet
gnoman wallet generate --name mywallet

# Generate with vanity address (prefix "00")
gnoman wallet generate --name vanity --vanity 00

# Import wallet from private key
gnoman wallet import --name imported --private-key 0x1234...

# List all wallets
gnoman wallet list
```

#### Safe Operations

```bash
# List all Safes
gnoman safe list

# List Safe owners
gnoman safe list-owners --name mysafe
```

#### Audit Operations

```bash
# Verify audit log integrity
gnoman audit run

# Show audit summary
gnoman audit summary

# Show recent logs
gnoman audit tail --lines 20
```

#### System Info

```bash
# Display system information
gnoman info
```

## Configuration

GNOMAN stores configuration in `~/.gnoman/`:
- `config.json` - Main configuration
- `audit_logs/` - Audit log files
- `abi_cache/` - Cached contract ABIs

### Environment Variables

Create a `.env` file or set environment variables:

```bash
ETH_RPC_URL=http://localhost:8545
CHAIN_ID=1
NETWORK_NAME=mainnet
```

## Architecture Demo

Run the architecture demo to see GNOMAN's design:

```bash
python3 examples/architecture_demo.py
```

## Security

- Private keys are stored in your system's keyring (Keychain, SecretService, or Windows Credential Manager)
- Private keys are NEVER written to disk
- Export/import uses ChaCha20-Poly1305 AEAD encryption with Scrypt KDF
- All actions are logged with hash-chain verification

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v

# Run with coverage
pytest --cov=gnoman --cov-report=html
```

## Next Steps

1. **Set up your RPC connection** - Configure `ETH_RPC_URL` in `.env` or pass `--rpc-url`
2. **Create your first wallet** - Use `gnoman wallet generate --name mywallet`
3. **Load a Safe** - In the TUI, navigate to the Safes tab
4. **Explore the audit logs** - Check the Audit tab to see all recorded actions

## Troubleshooting

### Dependencies not installing

If you encounter network issues during installation, try:
```bash
pip install --no-cache-dir -e .
```

### Keyring backend not available

On Linux, you may need to install:
```bash
# Ubuntu/Debian
sudo apt-get install gnome-keyring

# Fedora
sudo dnf install gnome-keyring
```

## Support

For issues or questions, please open an issue on GitHub.
