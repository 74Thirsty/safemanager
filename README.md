# GNOMAN - Mission Control Console for Blockchain Ecosystem

**GNOMAN** (short for *Gnosis + Key Manager*) is a **mission control console** for your blockchain ecosystem — a **local, secure, and fully interactive dashboard** that lets you:

* 🔐 Manage **wallets, private keys, and Safe multisigs**
* 🔑 Audit and rotate **secrets in the OS keyring**
* 📜 Interact with **smart contracts via custom ABIs**
* 🧪 Simulate **on-chain transactions** safely before executing
* 🔄 Sync everything with your **keyring, filesystem, and Ethereum RPC**

It's essentially **a local Gnosis Safe client, key manager, and contract cockpit**, combined into one **text-based GUI** (built with [Textual](https://github.com/Textualize/textual)) — running entirely offline, using your OS's native secret storage (Keychain, SecretService, or Windows Credential Manager).

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/74Thirsty/safemanager.git
cd safemanager

# Install with pip
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Run GNOMAN

```bash
# Launch the interactive dashboard
gnoman run

# Or with custom RPC
gnoman run --rpc-url http://localhost:8545

# Show system info
gnoman info
```

---

## 💡 Core Philosophy

GNOMAN is:

* **Deterministic:** All secrets, keys, and actions are reproducible and logged.
* **Offline-first:** No external API dependency for local key/contract operations.
* **Cross-platform:** Linux, macOS, and Windows.
* **Human-readable:** Rich UI, color-coded telemetry, and concise forensic logs.
* **Modular:** Each "pane" (Wallets, Safes, ABIs, etc.) is self-contained.

---

## 🏗️ Architecture

### Project Structure

```
gnoman/
├── utils/              # Crypto, keyring, env, and ABI utilities
│   ├── keyring_backend.py
│   ├── crypto_tools.py
│   ├── abi_tools.py
│   └── env_tools.py
├── core/               # Core logic modules
│   ├── wallet_manager.py
│   ├── safe_manager.py
│   ├── audit_manager.py
│   └── contract_manager.py
├── ui/                 # Textual-based UI
│   ├── app.py
│   ├── components/
│   └── screens/
└── main.py            # CLI entry point
```

### Core Modules

#### 🧩 `core/wallet_manager.py`
* Generate/import/export wallets
* Derive vanity addresses
* Track wallet metadata (balance, chain ID)
* Interface with Web3

#### 🧠 `core/safe_manager.py`
* Load Safe contracts via ABI
* Display owners, thresholds
* Prepare and sign SafeTx bundles
* Support Gnosis transaction simulation

#### 🗝️ `utils/keyring_backend.py`
* Abstract system keyring
* List, get, set, and delete secrets
* Export/import with encryption (ChaCha20-Poly1305)
* Audit stale or duplicate entries

#### 📜 `core/audit_manager.py`
* Write structured JSONL logs for all actions
* Verify with hash chains
* Expose last N logs to the dashboard

#### ⚡ `utils/abi_tools.py`
* Load and parse user-supplied ABIs
* Simulate functions locally (eth_call)
* Store tested ABIs to cache
* Validate inputs/outputs

---

## 🖥️ UI Layout

The Textual-based interface provides 7 tabs:

```
┌───────────────────────────────────────────────┐
│  Header: RPC · Network · Gas · Keyring Drift │
├───────────────────────────────────────────────┤
│ [Overview] [Wallets] [Safes] [Contracts] [Audit] [Sync] [Secrets] │
├───────────────────────────────────────────────┤
│ [ Main panel – content switches dynamically ] │
├───────────────────────────────────────────────┤
│  Footer: forensic log tail                   │
└───────────────────────────────────────────────┘
```

### Tab Features

* **Overview:** Network metrics, keyring drift, audit summary
* **Wallets:** Create/import/vanity wallet + balances
* **Safes:** Owners, threshold, queued transactions
* **Contracts:** Load custom ABI and test functions
* **Audit:** Tail logs + verification status
* **Sync:** Reconcile env ↔ keyring ↔ local config
* **Secrets:** Inspect and rotate credentials

---

## 🔒 Security Model

* Uses **`keyring`** (system backend) for secret storage
* **Never writes private keys to disk**
* For export/import: encrypted JSON container (with password-derived key)
* Uses **ChaCha20-Poly1305** AEAD and Scrypt KDF
* Optional **audit signing key** to verify all actions

---

## 📖 CLI Usage

### Wallet Commands

```bash
# Generate a new wallet
gnoman wallet generate --name mywallet

# Generate vanity address
gnoman wallet generate --name vanity --vanity 00

# Import wallet from private key
gnoman wallet import --name imported --private-key 0x123...

# List all wallets
gnoman wallet list
```

### Safe Commands

```bash
# List all Safes
gnoman safe list

# List Safe owners
gnoman safe list-owners --name mysafe
```

### Audit Commands

```bash
# Verify audit log integrity
gnoman audit run

# Show audit summary
gnoman audit summary

# Show recent logs
gnoman audit tail --lines 20
```

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v

# Format code
black gnoman/

# Type checking
mypy gnoman/
```

### Build Distribution

```bash
# Build package
python3 -m build

# Install locally
pip install dist/gnoman-2.0.0-py3-none-any.whl
```

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=gnoman --cov-report=html

# Run specific test file
pytest tests/test_wallet_manager.py -v
```

---

## 🔧 Configuration

GNOMAN stores configuration in `~/.gnoman/`:

* `config.json` - Main configuration
* `audit_logs/` - Audit log files
* `abi_cache/` - Cached contract ABIs

### Environment Variables

Create a `.env` file or set environment variables:

```bash
ETH_RPC_URL=http://localhost:8545
CHAIN_ID=1
NETWORK_NAME=mainnet
```

---

## 🎯 Headless Mode

GNOMAN supports headless CLI for automation:

```bash
gnoman wallet generate --name test
gnoman safe list-owners --name mysafe
gnoman audit run
```

---

## 🚧 Future Extensions

* 🔒 **Ledger/Trezor** wallet connector
* 🌐 **RPC switching** (Ethereum, Arbitrum, Base, etc.)
* 🧠 **AI audit assistant** (log analyzer using local ML)
* 📦 **Plugin system** (custom ABI-driven dashboards)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ✨ In Short

> GNOMAN is a **local, auditable, text-based command center** for your crypto ops —
> combining a **Gnosis Safe manager**, **keyring vault**, and **ABI testing console** into one secure TUI.