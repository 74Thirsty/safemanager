# Contributing to GNOMAN

Thank you for your interest in contributing to GNOMAN! This document provides guidelines for contributing to the project.

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/safemanager.git
   cd safemanager
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_wallet_manager.py -v

# Run with coverage
pytest --cov=gnoman --cov-report=html
```

### 4. Format Code

```bash
# Format with black
black gnoman/

# Check types
mypy gnoman/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Add feature: description"
```

Use clear, descriptive commit messages:
- `feat: Add vanity address generation`
- `fix: Resolve keyring authentication issue`
- `docs: Update installation instructions`
- `test: Add tests for audit manager`

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Project Structure

```
gnoman/
├── utils/          # Utility modules
│   ├── keyring_backend.py
│   ├── crypto_tools.py
│   ├── abi_tools.py
│   └── env_tools.py
├── core/           # Core business logic
│   ├── wallet_manager.py
│   ├── safe_manager.py
│   ├── audit_manager.py
│   └── contract_manager.py
├── ui/             # Textual UI components
│   ├── app.py
│   ├── components/
│   └── screens/
└── main.py         # CLI entry point
```

## Coding Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

### Documentation

- Add docstrings to all public methods
- Update README.md for major features
- Add examples for new functionality

### Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use pytest fixtures for common setup
- Mock external dependencies (keyring, web3)

### Security

- Never commit secrets or private keys
- Use the keyring backend for sensitive data
- Validate all user inputs
- Follow secure coding practices

## Areas for Contribution

### High Priority

- [ ] Additional UI components for Textual app
- [ ] More comprehensive Safe contract interactions
- [ ] Hardware wallet integration (Ledger/Trezor)
- [ ] Additional network support (Arbitrum, Base, etc.)

### Medium Priority

- [ ] Enhanced ABI testing and validation
- [ ] Transaction simulation improvements
- [ ] Export/import format extensions
- [ ] Performance optimizations

### Documentation

- [ ] Tutorial videos or guides
- [ ] API documentation
- [ ] Example use cases
- [ ] Troubleshooting guides

## Testing Your Changes

### Unit Tests

```bash
pytest tests/test_wallet_manager.py -v
```

### Integration Tests

```bash
# With a local RPC node running
pytest tests/integration/ -v
```

### Manual Testing

1. Run the TUI: `gnoman run`
2. Test CLI commands: `gnoman wallet list`
3. Verify no regressions in existing functionality

## Submitting Pull Requests

### PR Checklist

- [ ] Tests pass locally
- [ ] Code is formatted with black
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Changes are focused and minimal

### PR Description

Include in your PR description:
- What problem does this solve?
- How does it solve it?
- Any breaking changes?
- Screenshots (for UI changes)
- Related issues

## Getting Help

- Open an issue for bugs or feature requests
- Tag issues appropriately (bug, enhancement, question)
- Provide minimal reproducible examples for bugs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to GNOMAN! 🚀
