#!/usr/bin/env python3
"""Generate ASCII art diagram of GNOMAN architecture"""

ARCHITECTURE = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    GNOMAN MISSION-CONTROL CONSOLE                         ║
║                   Production-Ready Architecture                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                            │
│                         (Textual Framework)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐   ┌────────────────────────────────────────────────┐  │
│  │ SPLASH       │──▶│           DASHBOARD (Main Screen)              │  │
│  │ SCREEN       │   │                                                 │  │
│  └──────────────┘   │  ┌─────────┬─────────┬───────────┬──────────┐ │  │
│                     │  │ Wallets │ Safes   │ Contracts │  Audit   │ │  │
│                     │  │   Tab   │   Tab   │    Tab    │   Tab    │ │  │
│                     │  ├─────────┼─────────┼───────────┼──────────┤ │  │
│                     │  │  Sync   │ Secrets │           │          │ │  │
│                     │  │   Tab   │   Tab   │           │          │ │  │
│                     │  └─────────┴─────────┴───────────┴──────────┘ │  │
│                     └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐           │
│  │  Tab Managers  │  │  Data Models   │  │   Utilities     │           │
│  ├────────────────┤  ├────────────────┤  ├─────────────────┤           │
│  │ • WalletsTab   │  │ • WalletModel  │  │ • Web3Manager   │           │
│  │ • SafesTab     │  │ • SafeModel    │  │ • StorageManager│           │
│  │ • ContractsTab │  │ • ContractModel│  │ • KeyringManager│           │
│  │ • AuditTab     │  │ • AuditModel   │  │ • SafeManager   │           │
│  │ • SyncTab      │  │ • SecretModel  │  │ • Config        │           │
│  │ • SecretsTab   │  │ • AppConfig    │  │                 │           │
│  └────────────────┘  └────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │  Web3.py │  │ Safe-ETH │  │ Keyring  │  │  Crypto  │               │
│  │          │  │          │  │          │  │          │               │
│  │ • RPC    │  │ • Safes  │  │ • Secure │  │ • Fernet │               │
│  │ • Wallet │  │ • Owners │  │   Store  │  │ • Hashing│               │
│  │ • Signs  │  │ • Txns   │  │ • System │  │          │               │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐        │
│  │  File Storage   │  │  System Keyring  │  │   Blockchain    │        │
│  ├─────────────────┤  ├──────────────────┤  ├─────────────────┤        │
│  │ ~/.gnoman/      │  │ • Private Keys   │  │ • Ethereum      │        │
│  │ ├─ wallets/     │  │ • Secrets        │  │ • Polygon       │        │
│  │ ├─ safes/       │  │ • Passphrases    │  │ • Testnets      │        │
│  │ ├─ contracts/   │  │ • API Keys       │  │ • Custom RPCs   │        │
│  │ ├─ audits/      │  │                  │  │                 │        │
│  │ └─ config.yaml  │  │ (Encrypted)      │  │ (Real-time)     │        │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘        │
└─────────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════╗
║                            KEY FEATURES                                   ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  🔐 SECURITY                  📊 DATA MANAGEMENT                         ║
║  • System keyring            • JSON storage                              ║
║  • Encrypted keys            • YAML config                               ║
║  • Audit logging             • Pydantic models                           ║
║  • No plaintext secrets      • Auto-save                                 ║
║                                                                           ║
║  🌐 WEB3 INTEGRATION         🎨 USER INTERFACE                           ║
║  • Multi-chain support       • Textual TUI                               ║
║  • Real-time balances        • Tabbed layout                             ║
║  • Transaction signing       • Keyboard shortcuts                        ║
║  • Contract interaction      • Dark/Light themes                         ║
║                                                                           ║
║  🏦 MULTISIG SUPPORT         🔄 SYNCHRONIZATION                          ║
║  • Gnosis Safe tracking      • Batch updates                             ║
║  • Owner management          • Progress tracking                         ║
║  • Threshold display         • Selective sync                            ║
║  • Pending transactions      • Last sync times                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

def main():
    print(ARCHITECTURE)

if __name__ == "__main__":
    main()
