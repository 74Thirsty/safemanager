# Contributing to GNOMAN

Thank you for your interest in contributing to GNOMAN! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Basic knowledge of Textual framework
- Understanding of Ethereum and Web3

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/safemanager.git
   cd safemanager
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

5. Run the demo to verify installation:
   ```bash
   python demo.py
   ```

## Code Style

### Python Style
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all classes and functions

### Example:
```python
def get_balance(self, address: str, chain_id: int) -> Optional[str]:
    """Get balance for an address on a specific chain.
    
    Args:
        address: Ethereum address
        chain_id: Blockchain network ID
        
    Returns:
        Balance in ETH as string, or None if error
    """
    pass
```

### Textual Components
- Keep components modular
- Use CSS for styling
- Follow Textual best practices
- Maintain consistent layout patterns

## Project Structure

```
src/gnoman/
├── core/           # Core application components
├── tabs/           # Tab implementations
├── models/         # Data models
└── utils/          # Utility functions
```

### Adding a New Tab

1. Create file in `src/gnoman/tabs/`:
   ```python
   from textual.containers import Container
   from textual.widgets import DataTable, Button
   
   class MyTab(Container):
       """My new tab"""
       
       def compose(self) -> ComposeResult:
           yield Button("Click me")
   ```

2. Add to dashboard in `src/gnoman/core/dashboard.py`:
   ```python
   from gnoman.tabs.my_tab import MyTab
   
   # In Dashboard.compose():
   with TabPane("MyTab", id="tab-mytab"):
       yield MyTab(...)
   ```

### Adding a New Model

1. Create model in `src/gnoman/models/data_models.py`:
   ```python
   class MyModel(BaseModel):
       """My data model"""
       name: str
       value: int
   ```

2. Add storage methods in `src/gnoman/utils/storage.py`:
   ```python
   def save_my_model(self, model: MyModel) -> bool:
       """Save model to disk"""
       pass
   ```

## Testing

### Manual Testing
```bash
# Run the application
gnoman

# Run the demo
python demo.py

# Test specific components
python -c "from gnoman.tabs.wallets_tab import WalletsTab; print('✓')"
```

### Testing Checklist
- [ ] All imports work
- [ ] Tab navigation works
- [ ] Data persistence works
- [ ] Keyboard shortcuts work
- [ ] Error handling works
- [ ] UI is responsive

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes:
   - Write clean, documented code
   - Follow style guidelines
   - Test your changes

3. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/my-feature
   ```

5. Create Pull Request:
   - Describe your changes
   - Reference any issues
   - Include screenshots for UI changes
   - List testing performed

### PR Review Process
- Maintainers will review your PR
- Address any feedback
- Once approved, PR will be merged

## Feature Requests

### Proposing New Features

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Use cases
   - Implementation ideas
   - Potential impact

### Feature Categories

**High Priority**:
- Security improvements
- Bug fixes
- Performance optimizations

**Medium Priority**:
- New integrations
- UI enhancements
- Documentation improvements

**Low Priority**:
- Nice-to-have features
- Experimental ideas

## Bug Reports

### Reporting Bugs

Include:
- GNOMAN version
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

### Example Bug Report

```markdown
**Environment**
- GNOMAN: 0.1.0
- Python: 3.10.5
- OS: Ubuntu 22.04

**Description**
Wallet creation fails when...

**Steps to Reproduce**
1. Open GNOMAN
2. Navigate to Wallets tab
3. Press 'n' to create wallet
4. Error occurs

**Expected**
Wallet should be created

**Actual**
Error: KeyError...

**Logs**
[paste error logs]
```

## Documentation

### Updating Documentation

When adding features:
- Update README.md
- Update FEATURES.md
- Update QUICKSTART.md
- Add code comments
- Update docstrings

### Documentation Style
- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep formatting consistent

## Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead:
1. Email maintainers directly
2. Provide detailed description
3. Include proof of concept if possible
4. Allow time for fix before disclosure

### Security Guidelines

- Never commit secrets
- Always encrypt sensitive data
- Use system keyring for credentials
- Validate all user input
- Log security events

## Code Review Guidelines

### For Reviewers

- Be constructive and respectful
- Provide specific feedback
- Suggest improvements
- Test the changes
- Approve when ready

### For Contributors

- Respond to feedback promptly
- Don't take criticism personally
- Ask questions if unclear
- Make requested changes
- Thank reviewers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue
- Check existing documentation
- Review similar PRs

## Resources

### Helpful Links
- [Textual Documentation](https://textual.textualize.io/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PEP 8 Style Guide](https://pep8.org/)

### Development Tools
- [Textual DevTools](https://textual.textualize.io/guide/devtools/)
- [Black](https://black.readthedocs.io/) - Code formatter
- [MyPy](https://mypy.readthedocs.io/) - Type checker
- [Pylint](https://pylint.org/) - Code linter

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commits (Co-authored-by)

Thank you for contributing to GNOMAN! 🚀
